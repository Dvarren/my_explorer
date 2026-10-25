from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from ..providers.base import FileEntry

class FileListModel(QAbstractListModel):
    NameRole = Qt.ItemDataRole.UserRole + 1
    IsDirRole = Qt.ItemDataRole.UserRole + 2
    EntryRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, entries: list[FileEntry] | None = None):
        super().__init__()
        self._entries = entries or []

    def set_entries(self, entries: list[FileEntry]):
        self.beginResetModel()
        self._entries = entries
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._entries)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        entry = self._entries[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            icon = "📁 " if entry.is_dir else "📄 "
            return icon + entry.name
            
        # Скрытые данные для логики
        if role == self.NameRole:
            return entry.name
        if role == self.IsDirRole:
            return entry.is_dir
        if role == self.EntryRole:
            return entry
            
        return None