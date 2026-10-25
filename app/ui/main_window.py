from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from .home_screen import HomeScreen
from ..infra.config import load_config
from ..providers.bundled import BundledProvider
from ..providers.local_folder import LocalFolderProvider
from ..providers.cloud import CloudProvider

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мой Проводник")
        
        cfg = load_config()
        self.providers = {
            "bundled": BundledProvider(),
            "local": LocalFolderProvider(cfg["local_folder"]),
            "cloud": CloudProvider()
        }

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_screen = HomeScreen(self)
        self.stack.addWidget(self.home_screen)

    def open_folder(self, provider_id: str):
        provider = self.providers.get(provider_id)
        QMessageBox.information(self, "Успех!", f"Вы выбрали: {provider.display_name}\nПуть: {provider.root}")