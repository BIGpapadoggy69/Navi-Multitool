from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPixmap
from .styles import MAIN_STYLE, SIDEBAR_STYLE, TOPBAR_STYLE, close_btn_style
from .pages.options_page import OptionsPage
from .pages.builder_page import BuilderPage
from .pages.info_page import InfoPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("modules/logos/navi_logo.png"))
        self.setWindowTitle("NAVI")
        self.setGeometry(100, 50, 1000, 700)
        self.setStyleSheet(MAIN_STYLE)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.dragging = False
        self.offset = QPoint()

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = self.create_top_bar()
        
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        
        self.sidebar = self.create_sidebar()
        
        self.stack = QStackedWidget()
        self.options_page = OptionsPage()
        self.builder_page = BuilderPage(self.options_page)
        self.info_page = InfoPage()
        
        self.stack.addWidget(self.options_page)
        self.stack.addWidget(self.builder_page)
        self.stack.addWidget(self.info_page)
        
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stack)

        main_layout.addWidget(top_bar)
        main_layout.addLayout(body_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        self.fade_anim = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.setEasingCurve(QEasingCurve.InOutQuad)

    def create_top_bar(self):
        top_bar = QFrame()
        top_bar.setFixedHeight(35)
        top_bar.setStyleSheet(TOPBAR_STYLE)
        
        top_bar.mousePressEvent = self.topbar_mousePressEvent
        top_bar.mouseMoveEvent = self.topbar_mouseMoveEvent
        top_bar.mouseReleaseEvent = self.topbar_mouseReleaseEvent
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(15, 0, 10, 0)
        top_layout.setSpacing(10)
        
        logo = QLabel()
        pixmap = QPixmap("modules/logos/navi_logo.png")
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("N")
            logo.setFont(QFont("Segoe UI", 16, QFont.Bold))
            logo.setStyleSheet("color: #00a2ff;")
        
        title = QLabel("NAVI")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title.setStyleSheet("color: #e0e0e0;")
        
        top_layout.addWidget(logo)
        top_layout.addWidget(title)
        top_layout.addStretch()

        btn_minimize = QPushButton("—")
        btn_close = QPushButton("X")
        
        btn_minimize.setStyleSheet("""
            QPushButton {
                text-align: center;
                background-color: transparent;
                color: #999;
                border: none;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
                min-width: 55px;
                max-width: 55px;
                min-height: 35px;
                max-height: 35px;
            }
            QPushButton:hover {
                background-color: #1a1a2a;
                color: #00a2ff;
            }
        """)
        btn_close.setStyleSheet(close_btn_style)
        
        btn_minimize.clicked.connect(self.showMinimized)
        btn_close.clicked.connect(self.close)
        
        top_layout.addWidget(btn_minimize)
        top_layout.addWidget(btn_close)
        
        top_bar.setLayout(top_layout)
        return top_bar
    
    def topbar_mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()
    
    def topbar_mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)
    
    def topbar_mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(150)
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        
        side_layout = QVBoxLayout()
        side_layout.setContentsMargins(10, 20, 10, 20)
        side_layout.setSpacing(5)

        self.btn_options = QPushButton("options")
        self.btn_builder = QPushButton("build")
        self.btn_info = QPushButton("info")

        self.btn_options.setObjectName("active")

        self.btn_options.clicked.connect(lambda: self.switch_page(0, self.btn_options))
        self.btn_builder.clicked.connect(lambda: self.switch_page(1, self.btn_builder))
        self.btn_info.clicked.connect(lambda: self.switch_page(2, self.btn_info))
        
        side_layout.addWidget(self.btn_options)
        side_layout.addWidget(self.btn_builder)
        side_layout.addWidget(self.btn_info)
        side_layout.addStretch()
        
        footer = QLabel('<a href="https://github.com/glockinhand/navi-multitool" style="color: #888; text-decoration: none; font-size: 10px;">Navi Multitool</a>')
        footer.setOpenExternalLinks(True)
        footer.setAlignment(Qt.AlignCenter)
        side_layout.addWidget(footer)
        
        sidebar.setLayout(side_layout)
        return sidebar

    def switch_page(self, index, button):
        for btn in [self.btn_options, self.btn_builder, self.btn_info]:
            btn.setObjectName("")
            btn.setStyleSheet("")
        
        button.setObjectName("active")
        button.setStyleSheet(MAIN_STYLE)
        
        self.stack.setCurrentIndex(index)

    def showEvent(self, event):
        super().showEvent(event)
        self.fade_anim.start()
