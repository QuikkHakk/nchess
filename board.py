from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSvg import QSvgRenderer

import chess

from engine import EngineHandler
from arrow import draw_arrow

from math import floor
from constants import BLACK, WHITE

class ChessBoard(QWidget):
    def __init__(self, main_view):
        super().__init__()
        self.board_svg = QSvgRenderer("assets/boards/blue.svg")
        self.main_view = main_view
        self.board = chess.Board()
        self.piece_images = {}
        self.ranks = "87654321"
        self.files = "abcdefgh"
        self.move = WHITE
        self.board_size = 0
        self.tile_size = 0
        self.selected = None
        self.engine_handler = EngineHandler(self)
        self.best_move = None
        self.show_best_move = True
        self.move_history = []
        self.arrows = []
        self.dragging = False
        self.dragX = 0
        self.dragY = 0

        for c in "QRPBNK":
            self.piece_images[WHITE + c] = QSvgRenderer("assets/pieces/w" + c + ".svg")
            self.piece_images[BLACK + c] = QSvgRenderer("assets/pieces/b" + c + ".svg")

    def paintEvent(self, event):
        self.board_size = min(self.width(), self.height())
        self.tile_size = self.board_size / 8

        painter = QPainter()

        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

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

        for arrow in self.arrows:
            fx = arrow[0] * self.tile_size + self.tile_size / 2
            fy = arrow[1] * self.tile_size + self.tile_size / 2
            tx = arrow[2] * self.tile_size + self.tile_size / 2
            ty = arrow[3] * self.tile_size + self.tile_size / 2

            painter.setBrush(QBrush(QColor(34, 139, 34, 130), Qt.SolidPattern))
            painter.setPen(Qt.NoPen)

            painter.drawPolygon(draw_arrow(fx, fy, tx, ty, 40, 10))

        if self.best_move != None and self.show_best_move:
            bm = self.best_move
            fx, fy = self.coordsofsquare(bm.from_square)
            tx, ty = self.coordsofsquare(bm.to_square)
            
            fx = fx * self.tile_size + self.tile_size / 2
            fy = fy * self.tile_size + self.tile_size / 2
            tx = tx * self.tile_size + self.tile_size / 2
            ty = ty * self.tile_size + self.tile_size / 2

            painter.setBrush(QBrush(QColor(0, 92, 153, 130), Qt.SolidPattern))
            painter.setPen(Qt.NoPen)

            painter.drawPolygon(draw_arrow(fx, fy, tx, ty, 70, 15))

        painter.end()

        self.update()

    def mouse_press(self, event):
        if event.button() == Qt.RightButton:
            x = event.x()
            y = event.y()
            if x <= self.board_size and y <= self.board_size:
                tx = floor(x / self.tile_size)
                ty = floor(y / self.tile_size)

                self.dragging = True
                self.dragX = tx
                self.dragY = ty
            else:
                self.dragging = False
                self.arrows.clear()

    def mouse_release(self, event):
        if event.button() == Qt.RightButton and self.dragging:
            x = event.x()
            y = event.y()
            if x <= self.board_size and y <= self.board_size:
                tx = floor(x / self.tile_size)
                ty = floor(y / self.tile_size)

                if self.dragX != tx or self.dragY != ty:
                    already_arr = False
                    for arr in self.arrows:
                        # if arrow already exists, remove it
                        if arr[0] == self.dragX and arr[1] == self.dragY and arr[2] == tx and arr[3] == ty:
                            already_arr = True
                            self.arrows.remove(arr)
                    if not already_arr:
                        self.arrows.append((self.dragX, self.dragY, tx, ty))
            else:
                self.dragging = False

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
        self.board.push(move)
        self.selected = None
        self.engine_handler.analyze(self.board)
        self.main_view.fen_field.setText(self.fen())
        self.arrows.clear()
   
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

    def coordsofsquare(self, sq):
        return (chess.square_file(sq), 7 - chess.square_rank(sq))

    def coordstopos(self, x, y):
        return self.files[x] + self.ranks[y]

    def _domove(self):
        mv = self.move_history.pop()
        if mv != None:
            self.board.push(mv)
            self.main_view.fen_field.setText(self.board.fen())
        self.engine_handler.analyze(self.board)
        self.arrows.clear()

    def _undomove(self):
        try:
            self.move_history.append(self.board.pop())
        except:
            pass
        self.engine_handler.analyze(self.board)
        self.main_view.fen_field.setText(self.board.fen())
        self.arrows.clear()

    def startpos(self):
        self.loadfen(chess.STARTING_FEN)

    def loadfen(self, fen):
        self.move_history = []
        self.board.set_fen(fen)
        self.engine_handler.analyze(self.board)
        self.main_view.fen_field.setText(self.board.fen())

    def fen(self):
        return self.board.fen()

    def show_best_move_changed(self, state):
        self.show_best_move = state == Qt.Checked
    
    def change_engine(self, engine):
        self.engine_handler.change_engine(engine)
        self.engine_handler.stop_current()
        self.engine_handler.analyze(self.board)

    def set_best_move(self, best_move):
        self.best_move = best_move

    def next_move(self):
        if len(self.move_history) > 0:
            self._domove()
        else:
            if self.best_move != None:
                self.makemove(self.best_move)

    def back_move(self):
        self._undomove()

    def set_thoughts(self, pv):
        if len(pv) > 0:
            thoughts = "Engine thoughts: " + pv[0].uci()
            if len(pv) > 1:
                for m in range(1, len(pv)):
                    move = pv[m].uci()
                    thoughts += "->" + move
        self.main_view.engine_thoughts.setText(thoughts)

    def set_score(self, score):
        self.main_view.game_score.setText("Score: " + score)