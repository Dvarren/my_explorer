from pathlib import Path
from .base import StorageProvider, FileEntry

class LocalFolderProvider(StorageProvider):
    id = "local"
    display_name = "Моя папка"

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.root_label = self.root.name or str(self.root)

    def list_dir(self, rel_path: str = "") -> list[FileEntry]:
        base = self.root / rel_path
        if not base.is_dir():
            return []
        
        entries = []
        for child in sorted(base.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            entries.append(FileEntry(
                provider_id=self.id,
                path=str(Path(rel_path) / child.name).replace("\\", "/"),
                name=child.name,
                is_dir=child.is_dir()
            ))
        return entries