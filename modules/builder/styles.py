MAIN_STYLE = """
    QWidget {
        background-color: #0a0a1a;
        color: #e0e0e0;
        font-family: 'Segoe UI';
    }
    QPushButton {
        background-color: transparent;
        border: none;
        color: #bbb;
        font-size: 14px;
        padding: 12px 16px;
        text-align: left;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #1a1a2a;
        color: #00a2ff;
    }
    QPushButton#active {
        background-color: #1a1a2a;
        color: #00a2ff;
        border-left: 3px solid #00a2ff;
    }
    QLabel {
        font-size: 14px;
    }
    QCheckBox {
        color: #e0e0e0;
        font-size: 13px;
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #00a2ff;
        border-radius: 3px;
        background-color: transparent;
    }
    QCheckBox::indicator:checked {
        background-color: #00a2ff;
        border: 2px solid #00a2ff;
    }
    QLineEdit {
        background-color: #111122;
        border: 1px solid #2a2a3a;
        border-radius: 4px;
        padding: 8px;
        color: #e0e0e0;
        font-size: 13px;
    }
    QLineEdit:focus {
        border: 1px solid #00a2ff;
    }
    QComboBox {
        background-color: #111122;
        border: 1px solid #2a2a3a;
        border-radius: 4px;
        padding: 8px;
        color: #e0e0e0;
        font-size: 13px;
    }
    QComboBox:hover {
        border: 1px solid #00a2ff;
    }
    QPushButton#buildButton {
        text-align: center;
        background-color: #00a2ff;
        color: white;
        font-size: 14px;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 6px;
    }
    QPushButton#buildButton:hover {
        background-color: #00ccff;
    }
    QPushButton#iconButton {
        background-color: #111122;
        border: 1px solid #2a2a3a;
        color: #bbb;
        padding: 8px;
        border-radius: 4px;
    }
    QPushButton#iconButton:hover {
        border: 1px solid #00a2ff;
        color: #e0e0e0;
    }
    QPushButton#testButton {
        background-color: #00a2ff;
        color: white;
        font-size: 13px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 4px;
    }
    QPushButton#testButton:hover {
        background-color: #00ccff;
    }
    QScrollArea {
        border: none;
        background-color: transparent;
    }
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
"""

SIDEBAR_STYLE = """
    background-color: #0a0a15;
    border-right: 1px solid #1a1a2a;
"""

TOPBAR_STYLE = """
    QFrame {
        background-color: #0a0a15;
        border-bottom: 1px solid #1a1a2a;
    }
"""

SCROLL_STYLE = """
    QScrollArea {
        border: none;
    }
    QScrollBar:vertical {
        background: #111122;
        width: 8px;
        margin: 0px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #00a2ff;
        min-height: 25px;
        border-radius: 4px;
    }
"""

close_btn_style = """
    QPushButton {
        text-align: center;
        background-color: transparent;
        color: #999;
        border: none;
        font-size: 11px;
        font-weight: bold;
        padding: 0px;
        min-width: 45px;
        max-width: 45px;
        min-height: 35px;
        max-height: 35px;
    }
    QPushButton:hover {
        background-color: #ff4444;
        color: #fff;
    }
"""
