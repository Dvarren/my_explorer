from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtCore import Qt

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
        
        # ==========================================
        # 1. НАСТРОЙКА ФОНА (Двойная защита)
        # ==========================================
        base_dir = Path(__file__).resolve().parent.parent.parent
        bg_path = base_dir / "logo.jpg.png" 
        
        # Красим фон главного окна в белый цвет
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(Qt.white))
        self.setPalette(palette)

        # ==========================================
        # 2. ВАШ ФУНКЦИОНАЛ
        # ==========================================
        cfg = load_config()
        self.providers = {
            "bundled": BundledProvider(),
            "local": LocalFolderProvider(cfg["local_folder"]),
            "cloud": CloudProvider()
        }

        # Создаем контейнер для картинки (подложку)
        self.background_label = QLabel()
        self.background_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter) # <-- Выравниваем по ВЕРХУ и ЦЕНТРУ
        self.background_label.setStyleSheet("background-color: white;")
        
        if bg_path.exists():
            pixmap = QPixmap(str(bg_path))
            pixmap = pixmap.scaled(300, 299, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.background_label.setPixmap(pixmap)
        else:
            print(f"❌ ОШИБКА: Файл {bg_path} не найден!")

        # Создаем стек с кнопками
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: transparent;")

        # ==========================================
        # 3. СЛОЙ ДЛЯ ПОДНЯТИЯ КАРТИНКИ ВВЕРХ
        # ==========================================
        layout = QVBoxLayout(self.background_label)
        
        # Отступ сверху: если картинка все равно низко, сделайте 0 или -30.
        # Отступ снизу: 50, чтобы текст не прилипал к низу окна.
        layout.setContentsMargins(0, 20, 0, 50) 
        
        # Добавляем стек (кнопки) ПОВЕРХ картинки. 
        # Так как картинка выровнена по верху, текст "Выберите папку" 
        # теперь будет рисоваться строго над логотипом, а не на нем!
        layout.addWidget(self.stack)
        
        # Делаем подложку главным виджетом
        self.setCentralWidget(self.background_label)

        self.home_screen = HomeScreen(self)
        self.browser_screen = BrowserScreen(self)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.browser_screen)

    def open_folder(self, provider_id: str):
        provider = self.providers.get(provider_id)
        if not provider:
            return
        if provider_id == "cloud":
            QMessageBox.information(self, "Облако", "Мы сделаем это чуть позже!")
            return
        self.browser_screen.open_provider(provider, "")
        self.stack.setCurrentWidget(self.browser_screen)

    def show_home(self):
        self.stack.setCurrentWidget(self.home_screen)