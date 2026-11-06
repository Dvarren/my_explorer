import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Настройка иконки
    base_dir = Path(__file__).resolve().parent
    # ВАЖНО: У вас файл называется icon.png.png, поэтому пишем именно так!
    icon_path = base_dir / "icon.png.png" 
    
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    else:
        print(f"❌ Иконка не найдена по пути: {icon_path}")

    window = MainWindow()
    window.resize(1000, 600)
    window.show()
    
    sys.exit(app.exec())

    #Максим чмопс
    