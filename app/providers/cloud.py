from .base import StorageProvider

class CloudProvider(StorageProvider):
    id = "cloud"
    display_name = "Облако"
    root_label = "Облако"

    def list_dir(self, rel_path: str = []) -> list:
        return [] # Пока облако пустое