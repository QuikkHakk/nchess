from chess.engine import *
from chess import *

class EngineHandler(object):
    def __init__(self):
        self.stockfish = SimpleEngine.popen_uci("engines/stockfish/stockfish.exe")
        self.leela = SimpleEngine.popen_uci("engines/stockfish/stockfish.exe")
        self.engine = self.stockfish

    def analyze(self, board):
        info = self.engine.analyse(board, chess.engine.Limit(depth=12))
        print(info)

    def bestmove(self, board):
        info = self.engine.play(board, chess.engine.Limit(depth=12))
        print(info)

    def change_engine(self, to):
        if to == "Leela":
            self.engine = self.leela
        if to == "Stockfish":
            self.engine = self.stockfish 