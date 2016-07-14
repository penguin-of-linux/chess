class Player:
    def __init__(self, is_bot, team, level = 0):
        self.WHITE = 0
        self.BLACK = 1
        self.is_bot = is_bot
        self.team = team
        if (is_bot):
            self.level = level
        self.king_coords = (3, 0) if team == self.WHITE else (3, 7) #Исправить поиском короля, т.к. могут быть разные начальные позиции
        self.is_able_rokir_by_left = True
        self.is_able_rokir_by_right = True