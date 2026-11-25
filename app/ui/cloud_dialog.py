from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
import requests

app = QApplication.instance()
if app:
    app.setStyleSheet("QMessageBox { color: white; background-color: #2b2b2b; } "
                      "QMessageBox QLabel { color: white; } "
                      "QMessageBox QPushButton { background-color: #444; color: white; padding: 4px; }")


class CloudDialog(QDialog):
    def __init__(self, url: str = "http://localhost:8765", token: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подключение к облаку")
        self.setMinimumWidth(420)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("URL сервера:"))
        self.url_edit = QLineEdit(url)
        layout.addWidget(self.url_edit)

        layout.addWidget(QLabel("Токен доступа:"))
        self.token_edit = QLineEdit(token)
        self.token_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.token_edit)

        row = QHBoxLayout()
        test_btn = QPushButton("Проверить")
        test_btn.clicked.connect(self._test)
        ok_btn = QPushButton("Сохранить")
        ok_btn.clicked.connect(self._save)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        row.addWidget(test_btn)
        row.addStretch()
        row.addWidget(cancel_btn)
        row.addWidget(ok_btn)
        layout.addLayout(row)

        self.result_url = ""
        self.result_token = ""

    def _test(self):
        try:
            r = requests.get(
                self.url_edit.text().rstrip("/") + "/api/status", timeout=3
            )
            if r.ok:
                QMessageBox.information(self, "ОК", "Сервер отвечает.")
            else:
                QMessageBox.warning(self, "Ошибка", f"Сервер вернул {r.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться: {e}")

    def _save(self):
        url = self.url_edit.text().strip().rstrip("/")
        token = self.token_edit.text().strip()
        if not url or not token:
            QMessageBox.warning(self, "Ошибка", "Заполните оба поля")
            return
        try:
            r = requests.get(
                url + "/api/list",
                params={"path": ""},
                headers={"X-Auth-Token": token},
                timeout=3,
            )
            if r.status_code == 401:
                QMessageBox.warning(self, "Ошибка", "Неверный токен")
                return
            if not r.ok:
                QMessageBox.warning(self, "Ошибка", f"Сервер вернул {r.status_code}")
                return
        except Exception as e:
            print("\n=== ОШИБКА ПРИ ПОДКЛЮЧЕНИИ ===")
            print(repr(e))  # Это выведет точную причину в терминал
            print("==============================\n")
            QMessageBox.critical(self, "Ошибка", f"Сервер недоступен: {e}")
            return
        self.result_url = url
        self.result_token = token
        self.accept()