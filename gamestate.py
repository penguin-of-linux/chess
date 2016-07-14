from figures import *
class GameState:
    def __init__(self, player1, player2):
        WHITE = 0
        BLACK = 1
        self.board = [
                [Tower(WHITE), Horse(WHITE), Elf(WHITE), King(WHITE), Queen(WHITE), Elf(WHITE), Horse(WHITE), Tower(WHITE)],
                [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
                [Tower(BLACK), Horse(BLACK), Elf(BLACK), King(BLACK), Queen(BLACK), Elf(BLACK), Horse(BLACK), Tower(BLACK)],
            ]

        #self.board = [
        #        [0, 0, 0, King(WHITE), 0, 0, 0, 0],
        #        [0, 0, 0, Queen(WHITE), Queen(WHITE), Queen(WHITE), Queen(WHITE), Queen(WHITE)],
        #        [0, 0, 0,Queen(WHITE), 0, 0, 0, 0, 0],
        #        [0, 0, 0, 0, 0, 0, 0, 0],
        #        [0, 0, 0, 0, 0, 0, 0, 0],
        #        [0, 0, 0, 0, 0, 0, 0, 0],
        #        [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
        #        [Tower(BLACK), Elf(WHITE), 0, King(BLACK), 0, Elf(BLACK), 0, Tower(BLACK)]
        #    ]
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.last_move = ((None, None), (None, None))


    def change_player(self):
        """
        Меняет текущего игрока
        """
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1