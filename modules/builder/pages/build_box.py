from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BuildLogBox(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("NAVI builder")
        self.setFixedSize(500, 350)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0a1a;
                border: 1px solid #2a2a3a;
            }
            QLabel {
                color: #00a2ff;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #0a0a15;
                color: #00a2ff;
                border: 1px solid #2a2a3a;
                font-family: Consolas, monospace;
                font-size: 11px;
            }
            QPushButton {
                background-color: #1a1a2a;
                border: 1px solid #00a2ff;
                padding: 6px;
                color: #00a2ff;
            }
            QPushButton:hover {
                background-color: #2a2a3a;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("BUILD PROCESS")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Consolas", 12, QFont.Bold))

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setEnabled(False)

        layout.addWidget(title)
        layout.addWidget(self.log_box)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def add_log(self, text: str):
        self.log_box.append(text)
        self.log_box.verticalScrollBar().setValue(
            self.log_box.verticalScrollBar().maximum()
        )

    def finish(self):
        self.add_log("\nNAVI: build finished")
        self.close_btn.setEnabled(True)
