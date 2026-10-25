import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Привет, мир! PySide6 настроен.")
label.show()
sys.exit(app.exec())