from pydantic import BaseModel, SerializeAsAny
from pathlib import Path
from typing import Any
import os
import json

appdata_dir = os.getenv('LOCALAPPDATA') + "\\.rpideck"

class Params:
    name: str
    type: str
    data: Any

    def __init__(self, params: dict, data_obj):
        self.name = params.get("name")
        if not self.name or type(self.name) is not str:
            data_obj.reset()
        self.type = params.get("type")
        if not self.type or type(self.type) is not str:
            data_obj.reset()
        self.data = params.get("data")

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "data": self.data
        }
    
class ParamsItem(BaseModel):
    name: str
    type: str
    data: dict[str, Any]

class WidgetItem(BaseModel):
    row_span: int
    column_span: int
    x: int
    y: int
    image: str | None
    text: str | None
    params: list[ParamsItem] | None

class Widget:
    row_span: int
    column_span: int
    x: int
    y: int
    image: str | None
    text: str | None
    params: list[Params] | None

    def __init__(self, widget: dict, data_obj):
        self.row_span = widget.get('rowSpan')
        if not self.row_span or type(self.row_span) is not int:
            data_obj.reset()
        self.column_span = widget.get('columnSpan')
        if not self.column_span or type(self.column_span) is not int:
            data_obj.reset()
        self.x = widget.get('x')
        if not self.x or type(self.x) is not int:
            data_obj.reset()
        self.y = widget.get('y')
        if not self.y or type(self.y) is not int:
            data_obj.reset()
        self.image = widget.get('image')
        self.text = widget.get('text')
        for param in widget.get("params") or []:
            self.params.append(Params(param, data_obj))


    def to_dict(self):
        return {
            "rowSpan": self.row_span,
            "columnSpan": self.column_span,
            "x": self.x,
            "y": self.y,
            "image": self.image,
            "params": [param.to_dict() for param in self.params]
        }

class Grid:
    columns: int
    rows: int
    widgets: list[list[Widget]] = []

    def __init__(self, grid: dict, data_obj):
        self.columns = grid.get('columns')
        if not self.columns or type(self.columns) is not int:
            data_obj.reset()
        self.rows = grid.get('rows')
        if not self.rows or type(self.rows) is not int:
            data_obj.reset()
        if grid.get('widgets') == None:
            data_obj.reset()
        for page in grid.get('widgets') or []:
            self.widgets.append([Widget(widget, data_obj) for widget in page])


    def to_dict(self):
        widgets = []
        for page in self.widgets:
            widgets.append([widget.to_dict() for widget in page])

        return {
            "columns": self.columns,
            "rows": self.rows,
            "widgets": widgets
        }

class Data:
    grid: Grid
    recording: bool = False
    recording_paused: bool = False
    streaming: bool = False
    replay_buffer: bool = False
    host: str
    port: int
    password: str | None
    __config_path: Path
    def __init__(self):
        self.__config_path = os.path.join(appdata_dir, "config.json")
        with open(self.__config_path, 'r') as f:
            data = f.read()
            if data == '':
                self.reset()
            data: dict = json.loads(data)
        self.password = data.get('password')
        self.host = data.get('host')
        if not self.host or type(self.host) is not str:
            self.reset()
        self.port = data.get('port')
        if not self.port or type(self.port) is not int:
            self.reset()
        if not data.get('grid'):
            self.reset()
        self.grid = Grid(data.get('grid'), self)

    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "password": self.password,
            "grid": self.grid.to_dict(),
        }
    
    def reset(self):
        with open(self.__config_path, 'w') as f:
            default = {
                "host": "localhost",
                "port": 4455,
                "password": None,
                "grid": {
                    "columns": 4,
                    "rows": 2,
                    "widgets": []
                }
            }
            json.dump(default, f)

    def save(self):
        with open(self.__config_path, 'w') as f:
            json.dump(self.to_dict(), f)

CONFIG = Data()