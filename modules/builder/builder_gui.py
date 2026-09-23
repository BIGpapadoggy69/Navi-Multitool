import sys
import os


_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from PyQt5.QtWidgets import QApplication
from modules.builder.main_window import MainWindow
from modules.builder.pages.splash import SplashScreen

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
