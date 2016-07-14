WHITE = 0
BLACK = 1

class Figure(): #Требуется для проверки на принадлежность к фигуре
    pass

class Pawn(Figure): #ID нужен для gui
    def __init__(self, color):
        self.color = color
        self.cost = 1
        self.ID = 1 if color == WHITE else -1

class Horse(Figure):
    def __init__(self, color):
        self.color = color
        self.cost = 2.5
        self.ID = 2 if color == WHITE else -2

class Elf(Figure):
    def __init__(self, color):
        self.color = color
        self.cost = 2.5
        self.ID = 3 if color == WHITE else -3

class Tower(Figure):
    def __init__(self, color):
        self.color = color
        self.cost = 5
        self.ID = 4 if color == WHITE else -4

class Queen(Figure):
    def __init__(self, color):
        self.color = color
        self.cost = 10
        self.ID = 5 if color == WHITE else -5

class King(Figure):
    def __init__(self, color):
        self.color = color
        self.cost = 100500
        self.ID = 6 if color == WHITE else -6