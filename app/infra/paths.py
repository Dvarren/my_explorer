import sys
import os
from pathlib import Path

def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent

def resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return app_dir() / relative_path

def data_dir() -> Path:
    d = app_dir() / "data"
    d.mkdir(exist_ok=True)
    return d

def user_config_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path.home() / ".config"
    d = base / "MyExplorer"
    d.mkdir(parents=True, exist_ok=True)
    return d