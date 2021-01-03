import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from chess import STARTING_FEN

from borderlayout import BorderLayout
from board import ChessBoard

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.board = ChessBoard(self)
        self.init()

    def init(self):
        self.create_menu()
        self.layout()

        self.setWindowTitle("NChess")
        self.setWindowIcon(QIcon("rsc/icon.png"))
        self.resize(1160, 900)

        self.center()

        self.show()

        self.board.startpos()

    def layout(self):
        layout = BorderLayout()
        layout.addWidget(self.board, BorderLayout.Center)

        vbox = QVBoxLayout()

        show_best_move = QCheckBox("Show Best Move")
        show_best_move.setChecked(True)
        show_best_move.stateChanged.connect(self.board.show_best_move_changed)
        vbox.addWidget(show_best_move)

        engine_selector = QComboBox()
        engine_selector.addItem("Stockfish")
        engine_selector.addItem("Leela")
        engine_selector.addItem("Komodo")
        engine_selector.currentIndexChanged.connect(lambda:self.board.change_engine(engine_selector.currentText()))
        vbox.addWidget(engine_selector)

        self.game_score = QLabel()
        self.game_score.setText("Score: 0")
        self.game_score.setWordWrap(True)
        self.game_score.setMaximumWidth(200)
        self.game_score.setMinimumWidth(200)
        vbox.addWidget(self.game_score)

        next_btn = QPushButton()
        next_btn.setText("Next")
        next_btn.clicked.connect(lambda:self.board.redo())
        vbox.addWidget(next_btn)

        undo_btn = QPushButton()
        undo_btn.setText("Back")
        undo_btn.clicked.connect(lambda:self.board.undo())
        vbox.addWidget(undo_btn)

        reset_btn = QPushButton()
        reset_btn.setText("Reset")
        reset_btn.clicked.connect(lambda:self.board.startpos())
        vbox.addWidget(reset_btn)

        self.fen_field = QLineEdit()
        self.fen_field.setText(STARTING_FEN)
        self.fen_field.setMinimumWidth(200)
        self.fen_field.setMaximumWidth(200)
        vbox.addWidget(self.fen_field)

        set_fen_btn = QPushButton()
        set_fen_btn.setText("Set fen")
        set_fen_btn.clicked.connect(lambda:self.board.loadfen(self.fen_field.text()))
        vbox.addWidget(set_fen_btn)

        self.engine_thoughts = QLabel()
        self.engine_thoughts.setText("...")
        self.engine_thoughts.setWordWrap(True)
        self.engine_thoughts.setMaximumWidth(200)
        self.engine_thoughts.setMinimumWidth(200)
        vbox.addWidget(self.engine_thoughts)

        vbox.addStretch(1)

        east_widget = QWidget()
        east_widget.setLayout(vbox)
        layout.addWidget(east_widget, BorderLayout.East)

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

    def closeEvent(self, event):
        self.board.engine_handler.stockfish.quit()
        self.board.engine_handler.leela.quit()
        self.board.engine_handler.komodo.quit()

app = QApplication(sys.argv)        
v = MainView()
sys.exit(app.exec_())