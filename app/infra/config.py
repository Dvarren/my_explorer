import json
from pathlib import Path
from .paths import app_dir

CONFIG_FILE = app_dir() / "config.json"

DEFAULTS = {
    "local_folder": str(Path.home() / "Documents") 
}

def load_config() -> dict:
    if not CONFIG_FILE.exists():
        save_config(DEFAULTS)
        return DEFAULTS
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return {**DEFAULTS, **json.load(f)}
    except:
        return DEFAULTS

def save_config(cfg: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)