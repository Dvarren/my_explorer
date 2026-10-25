import sys
from pathlib import Path

def app_dir() -> Path:
    """Возвращает папку, где лежит main.py (корень проекта)"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    
    # __file__ указывает на app/infra/paths.py
    # .parent -> app/infra
    # .parent.parent -> app
    # .parent.parent.parent -> my_explorer (наш корень)
    return Path(__file__).resolve().parent.parent.parent

def data_dir() -> Path:
    d = app_dir() / "data"
    d.mkdir(exist_ok=True)
    return d


if __name__ == "__main__":
    print("Путь к корню проекта:", app_dir())
    print("Путь к папке data:", data_dir())