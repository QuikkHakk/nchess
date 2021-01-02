import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.create_menu()

        self.setWindowTitle("NChess")
        self.setWindowIcon(QIcon("rsc/icon.png"))
        self.resize(800, 600)

        self.show()

    def create_menu(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")

        exit_action = QAction(QIcon("rsc/exit.png"), "Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file.addAction(exit_action)

app = QApplication(sys.argv)        
v = MainView()
sys.exit(app.exec_())