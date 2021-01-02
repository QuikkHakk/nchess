import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from borderlayout import BorderLayout
from board import ChessBoard

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board = ChessBoard()
        self.init()

    def init(self):
        self.create_menu()
        self.layout()

        self.setWindowTitle("NChess")
        self.setWindowIcon(QIcon("rsc/icon.png"))
        self.resize(800, 600)

        self.center()

        self.show()

    def layout(self):
        layout = BorderLayout()
        layout.addWidget(self.board, BorderLayout.Center)

        btn = QPushButton("test")
        layout.addWidget(btn, BorderLayout.East)

        btn2 = QPushButton("test")
        layout.addWidget(btn2, BorderLayout.East)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)

    def create_menu(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")

        exit_action = QAction(QIcon("rsc/exit.png"), "Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file.addAction(exit_action)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

app = QApplication(sys.argv)        
v = MainView()
sys.exit(app.exec_())