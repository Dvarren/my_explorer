from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt
from .home_screen import HomeScreen
from .browser_screen import BrowserScreen
from ..infra.config import load_config
from ..infra.config import save_config
from ..providers.bundled import BundledProvider
from ..providers.local_folder import LocalFolderProvider
from ..providers.cloud import CloudProvider
from .cloud_dialog import CloudDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мой Проводник")
        from ..infra.paths import resource_path
        bg_path = resource_path("logo.jpg.png")
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(Qt.white))
        self.setPalette(palette)
        cfg = load_config()
        self.providers = {
            "bundled": BundledProvider(),
            "local": LocalFolderProvider(cfg["local_folder"]),
            "cloud": CloudProvider()
        }
        self.background_label = QLabel()
        self.background_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.background_label.setStyleSheet("background-color: white;")
        if bg_path.exists():
            pixmap = QPixmap(str(bg_path))
            pixmap = pixmap.scaled(300, 299, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.background_label.setPixmap(pixmap)
        else:
            print(f"❌ ОШИБКА: Файл {bg_path} не найден!")
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(self.background_label)
        layout.setContentsMargins(0, 20, 0, 50)
        layout.addWidget(self.stack)
        self.setCentralWidget(self.background_label)
        self.home_screen = HomeScreen(self)
        self.browser_screen = BrowserScreen(self)
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.browser_screen)

    def open_folder(self, provider_id: str):
        if provider_id == "cloud":
            prov = self.providers["cloud"]
            if not prov.ping() or not prov.token:
                dlg = CloudDialog(url=prov.base or "http://localhost:8765", token=prov.token)
                if dlg.exec() != CloudDialog.Accepted:
                    return
                save_config({"cloud_url": dlg.result_url, "cloud_token": dlg.result_token})
                self.providers["cloud"] = CloudProvider()
                prov = self.providers["cloud"]
            self.browser_screen.open_provider(prov, "")
            self.stack.setCurrentWidget(self.browser_screen)
            return

        provider = self.providers.get(provider_id)
        if not provider:
            return
        self.browser_screen.open_provider(provider, "")
        self.stack.setCurrentWidget(self.browser_screen)

    def show_home(self):
        self.stack.setCurrentWidget(self.home_screen)