from dataclasses import dataclass

@dataclass
class FileEntry:
    provider_id: str  
    path: str         
    name: str         
    is_dir: bool      

class StorageProvider:
    id: str = ""
    display_name: str = ""
    root_label: str = "" 