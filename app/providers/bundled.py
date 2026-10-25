from .local_folder import LocalFolderProvider
from ..infra.paths import data_dir

class BundledProvider(LocalFolderProvider):
    id = "bundled"
    display_name = "Приложение"

    def __init__(self):
        super().__init__(str(data_dir()))
        self.root_label = "Приложение"