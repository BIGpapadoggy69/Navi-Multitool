from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont
from .build_box import BuildLogBox
from .message_box import CustomMessageBox
from ..functions.build_manager import BuildManager
import os


class BuildThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, compress, webhook_url, selected_payloads, file_name, file_type, file_icon_path, telegram_config):
        super().__init__()
        self.compress = compress
        self.webhook_url = webhook_url
        self.selected_payloads = selected_payloads
        self.file_name = file_name
        self.file_type = file_type
        self.file_icon_path = file_icon_path
        self.telegram_config = telegram_config
    
    def log(self, msg):
        self.log_signal.emit(msg)
    
    def run(self):
        try:
            success = BuildManager.buildFinal(
                compress=self.compress,
                webhook_url=self.webhook_url,
                selected_payloads=self.selected_payloads,
                file_name=self.file_name,
                file_type=self.file_type,
                file_icon_path=self.file_icon_path,
                telegram_config=self.telegram_config,
                log=self.log
            )
            
            if success:
                self.finished_signal.emit(True, "NAVI: build completed")
            else:
                self.finished_signal.emit(False, "NAVI: build failed")
                
        except Exception as e:
            self.log(f"\nNAVI: error - {str(e)}")
            self.finished_signal.emit(False, f"NAVI: build error")


class BuilderPage(QWidget):
    def __init__(self, options_page):
        super().__init__()
        self.options_page = options_page
        self.selected_icon = None
        self.build_thread = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        title = QLabel("build")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #00a2ff;")
        
        filename_layout = QVBoxLayout()
        filename_layout.setSpacing(6)
        filename_label = QLabel("file name")
        filename_label.setStyleSheet("color: #aaa; font-size: 12px;")
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("enter file name")
        self.filename_input.setMinimumHeight(38)
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        
        filetype_layout = QVBoxLayout()
        filetype_layout.setSpacing(6)
        filetype_label = QLabel("file type")
        filetype_label.setStyleSheet("color: #aaa; font-size: 12px;")
        self.filetype_combo = QComboBox()
        self.filetype_combo.addItems([".exe", ".py", ".pyw"])
        self.filetype_combo.setMinimumHeight(38)
        self.filetype_combo.currentTextChanged.connect(self.on_filetype_changed)
        filetype_layout.addWidget(filetype_label)
        filetype_layout.addWidget(self.filetype_combo)
        
        icon_layout = QVBoxLayout()
        icon_layout.setSpacing(6)
        self.icon_label = QLabel("exe icon")
        self.icon_label.setStyleSheet("color: #aaa; font-size: 12px;")
        self.icon_button = QPushButton("select icon")
        self.icon_button.setObjectName("iconButton")
        self.icon_button.setMinimumHeight(38)
        self.icon_button.clicked.connect(self.select_icon)
        self.icon_path_label = QLabel("no icon")
        self.icon_path_label.setStyleSheet("color: #555; font-size: 11px;")
        icon_layout.addWidget(self.icon_label)
        icon_layout.addWidget(self.icon_button)
        icon_layout.addWidget(self.icon_path_label)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.build_button = QPushButton("build")
        self.build_button.setObjectName("buildButton")
        self.build_button.setMinimumSize(160, 45)
        self.build_button.clicked.connect(self.start_build)
        button_layout.addWidget(self.build_button)
        button_layout.addStretch()
        
        main_layout.addWidget(title)
        main_layout.addLayout(filename_layout)
        main_layout.addLayout(filetype_layout)
        main_layout.addLayout(icon_layout)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        self.on_filetype_changed(self.filetype_combo.currentText())

    def on_filetype_changed(self, file_type):
        is_exe = file_type == ".exe"
        self.icon_label.setEnabled(is_exe)
        self.icon_button.setEnabled(is_exe)
        self.icon_path_label.setEnabled(is_exe)
        
        if not is_exe:
            self.selected_icon = None
            self.icon_path_label.setText("icon only for exe")
            self.icon_path_label.setStyleSheet("color: #555; font-size: 11px;")
        else:
            if not self.selected_icon:
                self.icon_path_label.setText("no icon")
                self.icon_path_label.setStyleSheet("color: #555; font-size: 11px;")

    def select_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "select icon", 
            "", 
            "Icon Files (*.ico);;All Files (*)"
        )
        
        if file_path:
            self.selected_icon = file_path
            name = file_path.split('/')[-1]
            self.icon_path_label.setText(name[:30])
            self.icon_path_label.setStyleSheet("color: #00a2ff; font-size: 11px;")

    def start_build(self):
        filename = self.filename_input.text().strip()
        if not filename:
            self.box = CustomMessageBox("NAVI", "error", "NAVI: enter file name")
            self.box.show()
            return
            
        filetype = self.filetype_combo.currentText()
        icon = self.selected_icon
        telegram_config = self.options_page.get_telegram_config()

        self.build_window = BuildLogBox(self)
        self.build_window.show()

        self.build_window.add_log("NAVI")
        self.build_window.add_log("")
        self.build_window.add_log(f"telegram: enabled")
        self.build_window.add_log(f"file: {filename}{filetype}")
        self.build_window.add_log("")

        full_path = f"output/{filename}"

        self.build_thread = BuildThread(
            compress=True,
            webhook_url="",
            selected_payloads=[],
            file_name=full_path,
            file_type=filetype.replace(".", ""),
            file_icon_path=icon,
            telegram_config=telegram_config
        )

        self.build_thread.log_signal.connect(self.build_window.add_log)
        self.build_thread.finished_signal.connect(self.on_build_finished)

        self.build_button.setEnabled(False)
        self.build_button.setText("building...")

        self.build_thread.start()

    def on_build_finished(self, success, message):
        self.build_window.add_log("")
        self.build_window.add_log(message)
        self.build_window.finish()
        
        self.build_button.setEnabled(True)
        self.build_button.setText("build")
        
        self.build_thread = None
