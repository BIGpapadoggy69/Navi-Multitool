import sys
from PyQt5.QtWidgets import QApplication
from builder.main_window import MainWindow
from builder.pages.splash import SplashScreen

def main():
    app = QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.start()
    
    window = MainWindow()
    
    def on_splash_finished():
        window.show()
        
    splash.finished.connect(on_splash_finished)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
