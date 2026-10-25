from PySide6.QtWidgets import QMainWindow, QStackedWidget
from .home_screen import HomeScreen
from .browser_screen import BrowserScreen
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
        self.browser_screen = BrowserScreen(self)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.browser_screen)

    def open_folder(self, provider_id: str):
        """Вызывается из HomeScreen при клике на кнопку"""
        provider = self.providers.get(provider_id)
        if not provider:
            return
            
        if provider_id == "cloud":
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Облако", "Мы сделаем его чуть позже!")
            return

        self.browser_screen.open_provider(provider, "")
        self.stack.setCurrentWidget(self.browser_screen)

    def show_home(self):
        """Возвращает на главный экран с тремя кнопками"""
        self.stack.setCurrentWidget(self.home_screen)