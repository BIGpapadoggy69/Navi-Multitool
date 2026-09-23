from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QGraphicsOpacityEffect
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal

class SplashScreen(QWidget):
    finished = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 50, 1000, 700)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.logo_label = QLabel()
        pixmap = QPixmap("modules/logos/navi_logo.png")
        if not pixmap.isNull():
            self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo_label.setText("N")
            self.logo_label.setFont(QFont("Segoe UI", 100, QFont.Bold))
            self.logo_label.setStyleSheet("color: #00a2ff;")
        
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        
        self.name = QLabel("NAVI")
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.name.setStyleSheet("color: #00a2ff; margin-top: 20px;")
        layout.addWidget(self.name, alignment=Qt.AlignCenter)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(1200)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim.finished.connect(self.fade_out)

    def start(self):
        self.show()
        self.anim.start()

    def fade_out(self):
        QTimer.singleShot(1000, self._start_fade_out)

    def _start_fade_out(self):
        self.anim2 = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim2.setDuration(600)
        self.anim2.setStartValue(1)
        self.anim2.setEndValue(0)
        self.anim2.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim2.finished.connect(self.close)
        self.anim2.finished.connect(self.finished.emit)
        self.anim2.start()
