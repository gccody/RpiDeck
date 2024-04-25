import os
import sys
from pathlib import Path

class Appdata:
    platform = sys.platform
    appdata_dir: Path
    config_file_path: Path
    plugin_folder: Path
    log_file_path: Path

    def __init__(self):
        self.appdata_dir = os.path.join(os.getenv('LOCALAPPDATA'), '.rpideck')
        if not os.path.exists(self.appdata_dir):
            os.mkdir(self.appdata_dir)
        self.plugins_folder = os.path.join(self.appdata_dir, 'plugins')
        if not os.path.exists(self.plugins_folder):
            os.mkdir(self.plugins_folder)
        self.log_file_path = os.path.join(self.appdata_dir, 'rpideck-server.log')