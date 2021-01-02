from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSvg import QSvgRenderer

import chess

from engine import EngineHandler

from arrow import draw_arrow

from math import floor
from constants import BLACK, WHITE

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board_svg = QSvgRenderer("assets/boards/blue.svg")
        self.board = chess.Board()
        self.piece_images = {}
        self.ranks = "87654321"
        self.files = "abcdefgh"
        self.move = WHITE
        self.board_size = 0
        self.tile_size = 0
        self.selected = None
        self.engine_handler = EngineHandler()

        for c in "QRPBNK":
            self.piece_images[WHITE + c] = QSvgRenderer("assets/pieces/w" + c + ".svg")
            self.piece_images[BLACK + c] = QSvgRenderer("assets/pieces/b" + c + ".svg")

    def paintEvent(self, event):
        self.board_size = min(self.width(), self.height())
        self.tile_size = self.board_size / 8

        painter = QPainter()

        painter.begin(self)

        self.board_svg.render(painter, QRectF(0, 0, self.board_size, self.board_size))
        
        if self.selected != None:
            painter.setBrush(QBrush(QColor(0, 120, 255, 100), Qt.SolidPattern))
            painter.setPen(QPen(QColor(0, 120, 255, 100), Qt.SolidLine))
            sx = self.selected[0]
            sy = self.selected[1]
            painter.drawRect(sx * self.tile_size, sy * self.tile_size, self.tile_size, self.tile_size)

            for f in range(len(self.files)):
                for r in range(len(self.ranks)):
                    if sx == f and sy == r:
                        continue
                    if self.islegalmove(sx, sy, f, r):
                        x = f * self.tile_size + self.tile_size / 4
                        y = r * self.tile_size + self.tile_size / 4
                        painter.drawEllipse(x, y, self.tile_size / 2, self.tile_size / 2)

        for f in range(len(self.files)):
            for r in range(len(self.ranks)):
                sn = self.files[f] + self.ranks[r]
                s = chess.parse_square(sn)
                piece = self.board.piece_at(s)
                if piece != None:
                    ps = piece.symbol()
                    color = WHITE if ps.isupper() else BLACK 
                    renderer = self.piece_images[color + ps.upper()]
                    bounds = QRectF(f * self.tile_size, r * self.tile_size, self.tile_size, self.tile_size)
                    renderer.render(painter, bounds)

        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawPolygon(draw_arrow(200, 400, 400, 200))

        painter.end()

        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.selected = None
        if event.button() != Qt.LeftButton:
            return

        x = event.x()
        y = event.y()
        if x <= self.board_size and y <= self.board_size:
            tx = floor(x / self.tile_size)
            ty = floor(y / self.tile_size)
            pc = self.getpiece(tx, ty)

            if self.selected == None:
                if pc != None and pc.color == self.board.turn:
                    self.selected = (tx, ty)
            else:
                if pc != None:
                    if pc.color == self.board.turn:
                        self.selected = (tx, ty)
                    else:
                        self.makemoveiflegal(tx, ty)
                else:
                    self.makemoveiflegal(tx, ty)
        else:
            self.selected = None

    def islegalmove(self, fx, fy, tx, ty):
        lm = self.board.legal_moves
        f = self.coordstopos(fx, fy)
        t = self.coordstopos(tx, ty)
        move = chess.Move.from_uci(f + t)
        return move in lm

    def makemove(self, move):
        self.engine_handler.bestmove(self.board)
    
        self.board.push(move)
        self.selected = None

    def makemoveiflegal(self, x, y):
        lm = self.board.legal_moves
        sx = self.selected[0]
        sy = self.selected[1]
        f = self.coordstopos(sx, sy)
        t = self.coordstopos(x, y)
        move = chess.Move.from_uci(f + t)
        if move in lm:
            self.makemove(move)
        else:
            # try with promotion
            move = chess.Move.from_uci(f + t + "q")
            if move in lm:
                self.makemove(move)

    def haspiece(self, x, y):
        return self.getpiece(x, y) != None

    def getpiece(self, x, y):
        s = chess.parse_square(self.files[x] + self.ranks[y])
        piece = self.board.piece_at(s)
        return piece

    def coordstopos(self, x, y):
        return self.files[x] + self.ranks[y]

    def startpos(self):
        self.board.set_fen(chess.STARTING_FEN)

    def loadfen(self, fen):
        self.board.set_fen(fen)

    def fen(self):
        return self.board.fen()
