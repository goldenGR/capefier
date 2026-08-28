import os
import sys

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

COMMON_PATHS = {
    "default": "%appdata%/.minecraft",
    "lunarClient": "user/.lunarclient/shared",
    "prismLauncher": "%appdata%/PrismLauncher",
    "forge": "user/curseforge/minecraft/Install",
    "modrinth": "%appdata%/com.modrinth.theseus/meta/assets/skins",
}


def expand_common_path(raw_path: str) -> str:
    path = raw_path

    appdata = os.environ.get("APPDATA", "") 
    path = path.replace("%appdata%", appdata)

    if path.startswith("user/"):
        path = os.path.join(os.path.expanduser("~"), path[len("user/"):])

    path = os.path.expandvars(path)
    path = os.path.normpath(path)
    return path


class MinecraftPathDialog(QDialog):

    def __init__(self, parent=None, common_paths: dict | None = None):
        super().__init__(parent)
        self.setWindowTitle("Select Minecraft Folder")
        self.setMinimumWidth(420)
        self.setModal(True)

        self.common_paths = common_paths or COMMON_PATHS
        self.selected_path: str | None = None

        self._build_ui()
        self._populate_dropdown()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Detected folders:"))
        self.combo = QComboBox(self)
        layout.addWidget(self.combo)

        layout.addWidget(QLabel("Or enter a custom folder:"))
        custom_row = QHBoxLayout()
        self.custom_input = QLineEdit(self)
        self.custom_input.setPlaceholderText("C:/path/to/folder")
        browse_btn = QPushButton("Browse...", self)
        browse_btn.clicked.connect(self._browse_folder)
        custom_row.addWidget(self.custom_input)
        custom_row.addWidget(browse_btn)
        layout.addLayout(custom_row)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        select_btn = QPushButton("Select", self)
        select_btn.setDefault(True)
        cancel_btn = QPushButton("Cancel", self)
        select_btn.clicked.connect(self._on_select)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(select_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _populate_dropdown(self):
        found = {}
        for label, raw in self.common_paths.items():
            expanded = expand_common_path(raw)
            if os.path.isdir(expanded):
                found[label] = expanded

        ordered_labels = []
        if "default" in found:
            ordered_labels.append("default")
        ordered_labels += [l for l in self.common_paths if l in found and l != "default"]

        for label in ordered_labels:
            self.combo.addItem(f"{label}  ({found[label]})", found[label])

        if self.combo.count() == 0:
            self.combo.addItem("No known folders found", None)
            self.combo.setEnabled(False)

    def _browse_folder(self):
        start_dir = self.custom_input.text().strip() or os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", start_dir)
        if folder:
            self.custom_input.setText(folder)

    def _on_select(self):
        custom = self.custom_input.text().strip()
        if custom:
            if not os.path.isdir(custom):
                QMessageBox.warning(
                    self, "Invalid folder",
                    "The custom path you entered doesn't exist:\n" + custom
                )
                return
            self.selected_path = os.path.normpath(custom)
        else:
            data = self.combo.currentData()
            if not data:
                QMessageBox.warning(self, "No folder selected",
                                     "Please pick a folder or enter a custom one.")
                return
            self.selected_path = data

        self.accept()

    @staticmethod
    def getPath(parent=None, common_paths: dict | None = None) -> str | None:
        owns_app = QApplication.instance() is None
        app = QApplication(sys.argv) if owns_app else QApplication.instance()

        dlg = MinecraftPathDialog(parent=parent, common_paths=common_paths)
        result = dlg.exec()

        if owns_app:
            pass

        if result == QDialog.Accepted:
            return dlg.selected_path
        return None


if __name__ == "__main__":
    path = MinecraftPathDialog.getPath()
    print("Selected path:", path)