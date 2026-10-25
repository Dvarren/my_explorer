from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("Выберите папку")
        title.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Кнопка 1
        btn_bundled = QPushButton("📁  Приложение")
        btn_bundled.clicked.connect(lambda: self.main_window.open_folder("bundled"))
        
        # Кнопка 2
        btn_local = QPushButton("💻  Моя папка")
        btn_local.clicked.connect(lambda: self.main_window.open_folder("local"))
        
        # Кнопка 3
        btn_cloud = QPushButton("☁️  Облако")
        btn_cloud.clicked.connect(lambda: QMessageBox.information(self, "Облако", "Мы сделаем его чуть позже!"))

        for btn in (btn_bundled, btn_local, btn_cloud):
            btn.setFixedSize(500, 100)
            btn.setStyleSheet("font-size: 24px; border-radius: 10px; background-color: #f0f0f0;")
            layout.addWidget(btn)