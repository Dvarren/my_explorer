import sys
from pathlib import Path

def app_dir() -> Path:
    #Папка где лежит main.py 
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent

def data_dir() -> Path:
    #Папка приложения - папка data рядом с программой
    d = app_dir() / "data"
    d.mkdir(exist_ok=True)
    return d