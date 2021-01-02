from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board_size = 0
        self.board_svg = QPixmap("assets/board/blue.svg")

    def paintEvent(self, event):
        self.board_size = min(self.width(), self.height())

        painter = QPainter()

        painter.begin(self)

        #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        #painter.setPen(Qt.NoPen)
        #painter.drawRect(0, 0, self.board_size, self.board_size)

        painter.drawPixmap(0, 0, self.board_size, self.board_size, self.board_svg)
        painter.end()

        self.update()