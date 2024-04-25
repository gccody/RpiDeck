import webbrowser
import pyautogui
from pathlib import Path
import subprocess
import psutil,os

class Link:
    __commandname__ = 'Link'

    @staticmethod
    async def execute(url: str):
        webbrowser.open(url=url)

class Text:
    __commandname__ = 'Text'

    @staticmethod
    async def execute(string: str):
        pyautogui.typewrite(string)

class HotKey:
    __commandname__ = 'Hotkey'

    @staticmethod
    async def execute(keys: list[str]):
        for key in keys:
            pyautogui.keyDown(key)
        for key in keys:
            pyautogui.keyUp(key)

class Open:
    __commandname__ = 'Open'

    @staticmethod
    async def execute(file_path: Path):
        DETACHED_PROCESS = 8
        subprocess.Popen(executable=file_path, creationflags=DETACHED_PROCESS, close_fds=True)

class Close:
    __commandname__ = 'Close'

    @staticmethod
    async def execute(program_name: str):
        for pid in (process.pid for process in psutil.process_iter() if process.name()==program_name):
            os.kill(pid)