import json
import sys
from pathlib import Path
from unpacker import CapePackManager
from sourcePathManager import MinecraftPathDialog

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QFileDialog,
    QHeaderView,
    QFrame,
)

from PySide6.QtGui import (
    QImage,
    QPixmap
)


DARK_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #1e1f22;
    color: #e0e0e0;
    font-family: Segoe UI, sans-serif;
    font-size: 13px;
}
QPushButton {
    background-color: #3a3d42;
    border: 1px solid #4a4d52;
    border-radius: 6px;
    padding: 8px 16px;
    color: #f0f0f0;
}
QPushButton:hover {
    background-color: #46494f;
}
QPushButton:pressed {
    background-color: #2f3136;
}
QPushButton#primary {
    background-color: #4c7bd9;
    border: none;
}
QPushButton#primary:hover {
    background-color: #5a89e6;
}
QTableWidget {
    background-color: #26282b;
    border: 1px solid #3a3d42;
    gridline-color: #3a3d42;
}
QHeaderView::section {
    background-color: #2f3136;
    color: #cfcfcf;
    padding: 6px;
    border: none;
}
QTextEdit {
    background-color: #17181a;
    border: 1px solid #3a3d42;
    border-radius: 4px;
    color: #9fdc9f;
    font-family: Consolas, monospace;
}
QLabel#header {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
}
QLabel#subtext {
    color: #9a9a9a;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cape Pack Manager")
        self.resize(720, 520)
        self.setAcceptDrops(True)

        self.manager = CapePackManager()

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        # Header
        header = QLabel("Cape Pack Manager")
        header.setObjectName("header")
        subtext = QLabel("Import a cape pack (.zip) and preview what it will replace.")
        subtext.setObjectName("subtext")
        root.addWidget(header)
        root.addWidget(subtext)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #3a3d42;")
        root.addWidget(line)

        # Button row
        btn_row = QHBoxLayout()
        self.import_btn = QPushButton("Import Cape Pack…")
        self.import_btn.setObjectName("primary")
        self.import_btn.clicked.connect(self.on_import_clicked)

        self.apply_btn = QPushButton("Apply Pack")
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self.on_apply_clicked)

        btn_row.addWidget(self.import_btn)
        btn_row.addWidget(self.apply_btn)
        btn_row.addStretch()
        root.addLayout(btn_row)

        # Package Info
        pckInfo_row = QHBoxLayout()
        self.packageIcon = QLabel()
        self.packageIcon.setFixedSize(48, 48)  
        self.packageIcon.setScaledContents(True)

        self.packageName = QLabel("Package Name")
        self.packageAuthor = QLabel("Package Author")

        self.packageName.setObjectName("header")
        self.packageAuthor.setObjectName("subtext")

        pckInfo_text_col = QVBoxLayout()
        pckInfo_text_col.setSpacing(2)
        pckInfo_text_col.addWidget(self.packageName)
        pckInfo_text_col.addWidget(self.packageAuthor)

        pckInfo_row.addWidget(self.packageIcon)
        pckInfo_row.addLayout(pckInfo_text_col)
        pckInfo_row.addStretch()

        root.addLayout(pckInfo_row)

        # File table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Cape Name", "File in Pack", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table, stretch=1)

        # Log panel
        log_label = QLabel("Log")
        log_label.setObjectName("subtext")
        root.addWidget(log_label)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(120)
        root.addWidget(self.log)

        self.log_msg("Ready. Import a cape pack to begin.")

    def on_import_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Cape Pack", "", "Cape Packs (*.zip *.cp)"
        )
        if not path:
            return
        self.load_pack(path)

    def load_pack(self, path: str):
        try:
            files = self.manager.load_pack(path, self.log_msg)
        except Exception as e:
            self.log_msg(f"Failed to read pack: {e}", error=True)
            return

        self.table.setRowCount(0)
        self.manifest = ""

        try:
            manifest_file = next((f for f in files if f.name == "manifest.json"), None)
            if not manifest_file: raise TypeError("Cant Load Package! \n Missing Manifest") 

            self.manifest = json.loads(manifest_file.read())

            # READ THE MANIFEST TO GET CONTENT!
            self.packCapes = self.manifest.get("capes") or None

            if self.packCapes == None:
                raise TypeError("Package doesnt contain any capes. Aborting")

            self.packTitle = self.manifest.get("packName") or None
            self.packAuthor = self.manifest.get("author") or None
            self.packIcon = self.manifest.get("packIcon") or None
            print(files)
            icon_entry = next(
                (f for f in files if f.name.lower() == self.packIcon),
                None
            )
            if icon_entry:
                icon_data = icon_entry.read()
                image = QImage()
                image.loadFromData(icon_data)
                self.packageIcon.setPixmap(QPixmap.fromImage(image))
            else:
                self.log_msg("Package Icon Not Found! (Ignoring)", True)

            self.packageName.setText(self.packTitle)
            self.packageAuthor.setText(self.packAuthor)

            self.capeEntryList = []
            for cape in self.packCapes:
                print(cape)

                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(cape))
                self.table.setItem(row, 1, QTableWidgetItem(self.packCapes[cape]))
                self.table.setItem(row, 2, QTableWidgetItem("Pending"))

                for f in files:
                    if f.name.lower() == self.manifest["capes"].get(cape).lower():
                        self.capeEntryList.append({cape: f}) 

            self.apply_btn.setEnabled(bool(files))
            self.log_msg(f"Loaded pack: {Path(path).name} ({len(files)} files)")

        except FileNotFoundError as e:
            self.log_msg(e, True)
        
        except Exception as e:
            self.log_msg(f"Failed to read pack: {e}", error=True)
            return

    def on_apply_clicked(self):
        path = MinecraftPathDialog.getPath()
        if not path:
            return
        try:
            self.manager.apply_pack(self.packCapes, self.capeEntryList, path, self.log_msg)
            self.log_msg("Pack applied successfully.")
        except NotImplementedError:
            self.log_msg("apply_pack() is not implemented yet — this is a stub.", error=True)
        except Exception as e:
            self.log_msg(f"Failed to apply pack: {e}", error=True)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path.lower().endswith(".zip") or path.lower().endswith(".cp"):
                self.load_pack(path)
            else:
                self.log_msg("Drop a .zip cape pack file.", error=True)

    # --- helpers ---------------------------------------------------------

    def log_msg(self, text: str, error: bool = False):
        color = "#ff8080" if error else "#9fdc9f"
        self.log.append(f'<span style="color:{color}">{text}</span>')


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()