import sys
import os
from pathlib import Path

def app_dir() -> Path:
    """Папка где лежит main.py"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent

def data_dir() -> Path:
    """Папка приложения data рядом с программой."""
    d = app_dir() / "data"
    d.mkdir(exist_ok=True)
    return d

def user_config_dir() -> Path:
    """Папка для настроек в AppData"""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path.home() / ".config"
        
    d = base / "MyExplorer"  # Название нашей программы
    d.mkdir(parents=True, exist_ok=True)
    return d