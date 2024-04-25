# Python Packages
import os
import sys
import json
import pystray
import logging
import pkgutil
import appdata
import inspect
import threading
import importlib.util
import multiprocessing
from pathlib import Path
from typing import get_type_hints

# Fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# GUI
import webview

# Misc
from PIL import Image, ImageDraw
from asyncio import ensure_future

# Local
from data import CONFIG, WidgetItem
from obs_client import obs_ws
from appdata import Appdata

if not sys.platform.startswith("win"):
    print("This system is not supported. Windows is the only supported server")
    sys.exit(0)

APP_NAME = "RpiDeck"
COMMANDS_DIR = 'commands'
 

# GUI setup
def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def load_module_from_path(path):
    """ Load a Python file as a module from a given path. """
    module_name = Path(path).stem  # Get the file name without extension as module name
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def register_commands_from_directory(directory_path):
    """ Load all .py files from a directory as modules and register their commands. """
    command_dict = {}
    for py_file in Path(directory_path).rglob('*.py'):
        if py_file.name != '__init__.py':  # Skip __init__.py files
            module = load_module_from_path(py_file)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, '__commandname__'):
                    command_name = getattr(obj, '__commandname__')
                    command_dict[command_name] = obj
    return command_dict

def get_command_args(func):
    """ Retrieve argument names and their types from a function, handling complex types like list."""
    type_hints = get_type_hints(func)
    args_info = {}
    for param_name, param_type in type_hints.items():
        # This will convert type hints into a readable format, like List[int] or str
        if hasattr(param_type, '__origin__'):
            # Handle complex types like List[int] or Dict[str, int]
            base_type = param_type.__origin__.__name__
            if hasattr(param_type, '__args__'):
                inner_types = ', '.join(t.__name__ for t in param_type.__args__)
                args_info[param_name] = f"{base_type}[{inner_types}]"
        else:
            # Handle simple types like int, str
            args_info[param_name] = param_type.__name__
    return args_info

def register_parsable_command_obj(directory_path):
    """ Load all .py files from a directory as modules and register their commands along with their arguments. """
    command_dict = {}
    for py_file in Path(directory_path).rglob('*.py'):
        if py_file.name != '__init__.py':  # Skip __init__.py files
            module = load_module_from_path(py_file)
            module_name = getattr(module, '__modulename__', module.__name__.split('.')[-1].capitalize())  # Optional: capitalize the module name
            if not command_dict.get(module_name):
                command_dict[module_name] = []
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, '__commandname__'):
                    command_name = getattr(obj, '__commandname__')
                    exec_method = getattr(obj, 'execute', None)
                    if callable(exec_method):
                        command_args = get_command_args(exec_method)
                        command_dict[module_name].append({ "commandName": command_name, "params": command_args })
    return command_dict


win = webview.create_window(APP_NAME, 'index.html')

def on_minimize():
    win.hide()

win.events.minimized += on_minimize

def restore_from_tray():
    win.show()
    win.restore()

def close_application():
    tray_icon.stop()
    win.destroy()
    sys.exit(0)

tray_icon = pystray.Icon(
    'RpiDeck',
    icon=create_image(64, 64, 'black', 'white')
)

tray_icon.menu = pystray.Menu(
    pystray.MenuItem("Restore", restore_from_tray, default=True),
    pystray.MenuItem("Quit", close_application)
)

# Initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Verify appdata files
appdata = Appdata()
logs = open(appdata.log_file_path, 'w')

# Set the output to file output if it is running in an exe
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    sys.stdout = logs
    sys.stderr = logs

    logger = logging.getLogger("uvicorn")
    logger.addHandler(logging.FileHandler(f"{appdata.appdata_dir}\\uvicorn.log"))
    logger.setLevel(logging.INFO)

# Register Commands
commands = register_commands_from_directory(COMMANDS_DIR)
commands.update(register_commands_from_directory(appdata.plugins_folder))
parsable_commands = register_parsable_command_obj(COMMANDS_DIR)
parsable_commands.update(register_parsable_command_obj(appdata.plugins_folder))

@app.get("/gridData")
async def grid_data():
    return JSONResponse(CONFIG.grid.to_dict())

@app.get("/commands")
async def parsable_commands_route():
    return JSONResponse(parsable_commands)

@app.post("/columns/{num_columns}")
async def update_columns(num_columns: int):
    CONFIG.grid.columns = num_columns
    CONFIG.save()

@app.post("/rows/{num_rows}")
async def update_rows(num_rows: int):
    CONFIG.grid.rows = num_rows
    CONFIG.save()

@app.patch("/widget")
async def widget(widget: WidgetItem):
    grid = []
    for _ in range(CONFIG.grid.rows):
        grid.append([0 for _ in range(CONFIG.grid.columns)])

async def handle_websocket_execution(websocket: WebSocket, callback, message_id, command_data):
    if not command_data:
        command_data = {}
    res = await callback(**command_data)
    if (res):
        await websocket.send_json({"name": "reply", "id": message_id, "datain": res, "dataout": command_data})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data: dict = json.loads(await websocket.receive_text())
                command_data = data.get("data")
                message_id = data.get("id")
                name = data.get("name")
                if name:
                    ensure_future(handle_websocket_execution(websocket, commands[name].execute, message_id, command_data))
                else:
                    pass
            except ValueError as e:
                pass
            
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    import uvicorn
    server_thread = threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": "0.0.0.0", "port": 8003, "reload": False})
    server_thread.daemon = True
    server_thread.start()
    tray_icon_thread = threading.Thread(target=tray_icon.run)
    tray_icon_thread.daemon = True
    tray_icon_thread.start()
    obs_ws.connect()
    webview.start()
