from pathlib import Path
import requests
import os
import tempfile
from PySide6.QtCore import QFileSystemWatcher, QTimer
from .base import StorageProvider, FileEntry

class CloudProvider(StorageProvider):
    id = "cloud"
    display_name = "Облако"

    def __init__(self):
        from ..infra.config import load_config
        cfg = load_config()
        self.base = (cfg.get("cloud_url") or "").rstrip("/")
        self.token = (cfg.get("cloud_token") or "").strip()
        self.root_label = "Облако"
        
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.headers.update({"X-Auth-Token": self.token})
        
        self._cache = {}

        self.watcher = QFileSystemWatcher()
        self.watcher.fileChanged.connect(self._on_file_changed)
        self._active_local_path = None
        self._active_remote_path = None

    def ping(self) -> bool:
        if not self.base:
            return False
        try:
            r = self.session.get(f"{self.base}/api/status", timeout=5)
            return r.ok
        except Exception:
            return False

    def list_dir(self, rel_path: str = "") -> list[FileEntry]:
        if not self.base or not self.token:
            return []
            
        if rel_path in self._cache:
            return self._cache[rel_path]
        
        r = self.session.get(
            f"{self.base}/api/list",
            params={"path": rel_path},
            timeout=15,
        )
        r.raise_for_status()
        
        entries = []
        for item in r.json().get("items", []):
            entries.append(FileEntry(
                provider_id=self.id,
                path=str(Path(rel_path) / item["name"]).replace("\\", "/"),
                name=item["name"],
                is_dir=item["is_dir"]
            ))
            
        self._cache[rel_path] = entries
        return entries

    def download(self, path: str, local: Path) -> Path:
        with self.session.get(
            f"{self.base}/api/download",
            params={"path": path},
            stream=True,
            timeout=60,
        ) as r:
            r.raise_for_status()
            with open(local, "wb") as f:
                for chunk in r.iter_content(65536):
                    f.write(chunk)
        return local

    def upload(self, local: Path, remote_dir: str = ""):
        with open(local, "rb") as f:
            r = self.session.post(
                f"{self.base}/api/upload",
                params={"path": remote_dir},
                files={"file": (local.name, f)},
                timeout=300,
            )
        r.raise_for_status()
        self._cache.clear()

    def mkdir(self, path: str):
        r = self.session.post(
            f"{self.base}/api/mkdir",
            json={"path": path},
            timeout=15,
        )
        r.raise_for_status()
        self._cache.clear()

    def delete(self, path: str):
        r = self.session.delete(
            f"{self.base}/api/delete",
            params={"path": path},
            timeout=15,
        )
        r.raise_for_status()
        self._cache.clear()

    def open_file(self, rel_path: str):
        temp_dir = Path(tempfile.gettempdir()) / "MyExplorerCloud"
        temp_dir.mkdir(exist_ok=True)
        
        local_path = temp_dir / Path(rel_path).name
        
        try:
            self.download(rel_path, local_path)
        except Exception as e:
            print(f"Не удалось скачать файл: {e}")
            return

        self._active_local_path = str(local_path)
        self._active_remote_path = str(Path(rel_path).parent).replace("\\", "/")
        if self._active_remote_path == ".":
            self._active_remote_path = ""
            
        if self._active_local_path in self.watcher.files():
            self.watcher.removePath(self._active_local_path)
        self.watcher.addPath(self._active_local_path)
        
        os.startfile(str(local_path))

    def _on_file_changed(self, filepath: str):
        if filepath == self._active_local_path:
            QTimer.singleShot(1500, self._sync_back)

    def _sync_back(self):
        if not self._active_local_path or not os.path.exists(self._active_local_path):
            return
        try:
            local_path = Path(self._active_local_path)
            self.upload(local_path, self._active_remote_path)
            print(f"✅ Файл {local_path.name} успешно сохранён в облако!")
        except Exception as e:
            print(f"❌ Ошибка синхронизации с облаком: {e}")