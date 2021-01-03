from chess.engine import *
from chess import *

import threading
import time

class EngineHandler(object):
    def __init__(self, game):
        self.stockfish = SimpleEngine.popen_uci("engines/stockfish/stockfish.exe")
        self.leela = SimpleEngine.popen_uci("engines/stockfish/stockfish.exe")
        self.komodo = SimpleEngine.popen_uci("engines/komodo/komodo.exe")
        self.engine = self.stockfish
        self.game = game
        self.stops = {}
        self.analysis_count = 0

    def analyze(self, board):
        for i in range(self.analysis_count):
            self.stops[i] = True
        self.stops[self.analysis_count] = False

        thread = threading.Thread(target=self.search_best_move, args=(board,self.analysis_count))
        thread.daemon = True
        thread.start()
        self.analysis_count += 1

    def search_best_move(self, board, ac):
        with self.engine.analysis(board) as analysis:
            for info in analysis:
                if self.stops[ac]:
                    analysis.stop()

                moves = info.get("pv")
                score = info.get("score")
                if score != None:
                    if score.is_mate():
                        self.game.set_score("Mate in " + str(score.relative.mate()))
                    else:
                        sc = score.relative.score()
                        self.game.set_score(str(sc / 100))
                if moves != None:
                    move = moves[0]
                    self.game.set_best_move(move)
                    self.game.set_thoughts(moves)

    def stop_current(self):
        self.stops[self.analysis_count-1] = True

    def change_engine(self, to):
        if to == "Leela":
            self.engine = self.leela
            print("Now using Leela engine")
        if to == "Stockfish":
            self.engine = self.stockfish 
            print("Now using Stockfish engine")
        if to == "Komodo":
            self.engine = self.komodo 
            print("Now using Komodo engine")