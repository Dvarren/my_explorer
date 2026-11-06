from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # Делаем фон прозрачным
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Создаем слой
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter) 
        
        # Отступы и пружинка для центрирования
        layout.setContentsMargins(0, 150, 0, 50) 
        layout.addStretch(1)
        
        # Заголовок
        title = QLabel("Выберите папку")
        title.setStyleSheet("font-size: 36px; font-weight: bold; margin-top: 120px; margin-bottom: 20px; color: #004394;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Кнопки
        btn_bundled = QPushButton("📁 Приложение")
        btn_bundled.clicked.connect(lambda: self.main_window.open_folder("bundled"))

        btn_local = QPushButton("💻 Моя папка")
        btn_local.clicked.connect(lambda: self.main_window.open_folder("local"))

        btn_cloud = QPushButton("☁️ Облако")
        btn_cloud.clicked.connect(lambda: self.main_window.open_folder("cloud"))

        # Настраиваем стили для кнопок
        for btn in (btn_bundled, btn_local, btn_cloud):
            btn.setFixedSize(350, 45) 
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 24px; 
                    border-radius: 15px; 
                    background-color: #004394; /* Темно-синий фон */
                    color: white; 
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563EB; /* СВЕТЛЕЕ при наведении */
                }
            """)
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        # Пружинка снизу (чтобы кнопки не прилипали к низу)
        layout.addStretch(1)

        # Общий стиль (прозрачность)
        self.setStyleSheet("QWidget { background-color: transparent; }")