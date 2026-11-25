from pathlib import PurePosixPath
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListView, QMessageBox
)
from PySide6.QtCore import Qt
from .file_model import FileListModel

class BrowserScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.provider = None
        self.current_path = ""

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        
        self.btn_back = QPushButton("← Назад")
        self.btn_back.setFixedSize(100, 40)
        self.btn_back.clicked.connect(self._go_back)
        
        self.btn_back.setStyleSheet("""
            QPushButton {
                color: #004394; 
                font-weight: bold; 
                font-size: 16px;
                background-color: white; 
                border: 2px solid #004394; 
                border-radius: 5px; 
            }
            QPushButton:hover {
                background-color: #E0E7FF; 
            }
        """)
        
        self.path_label = QLabel("Путь")
        self.path_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #004394;")
        
        top_bar.addWidget(self.btn_back)
        top_bar.addWidget(self.path_label, 1)
        
        layout.addLayout(top_bar)

        self.model = FileListModel()
        self.view = QListView()
        self.view.setModel(self.model)
        self.view.setStyleSheet("font-size: 18px; padding: 10px;")
        self.view.doubleClicked.connect(self._on_double_click)
        
        layout.addWidget(self.view, 1)

    def open_provider(self, provider, path: str = ""):
        self.provider = provider
        self.current_path = path
        self.refresh()

    def refresh(self):
        if not self.provider:
            return
            
        try:
            entries = self.provider.list_dir(self.current_path)
            self.model.set_entries(entries)
            self._update_path_label()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать папку:\n{e}")

    def _update_path_label(self):
        parts = [self.provider.root_label]
        if self.current_path:
            parts.extend(PurePosixPath(self.current_path).parts)
        self.path_label.setText(" / ".join(parts))

    def _go_back(self):
        if not self.current_path:
            self.main_window.show_home()
            return
            
        parent = str(PurePosixPath(self.current_path).parent)
        if parent == ".":
            parent = ""
            
        self.current_path = parent
        self.refresh()

    def _on_double_click(self, index):
        entry = self.model.data(index, FileListModel.EntryRole)
        if not entry:
            return

        if entry.is_dir:
            self.current_path = entry.path
            self.refresh()
        else:
            try:
                self.provider.open_file(entry.path)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")