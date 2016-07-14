import gui
import player
import time
import figures
import gamestate
import robot
from copy import deepcopy

WHITE = 0
BLACK = 1


class Game:

    def __init__(self, player1, player2):
        self.game_state = gamestate.GameState(player1, player2)
        self.render = gui.Render()
        self.render.init_board(self.game_state.board)


    def play(self):
        while True:
            """
            Получает ход игрока (независимо от того, является ли он ботом или нет), "делает ход" в game_state, 
            записывает ход в game_state.last_move, меняет игрока, обновляет картинку клеток, задействованных в
            ходе (ладья в рокировке, срубленная на проходе пешка)
            """
            temp_move = self.get_move()
            from_coords = temp_move[0]
            to_coords = temp_move[1]
            self.game_state.board[to_coords[1]][to_coords[0]] = self.game_state.board[from_coords[1]][from_coords[0]]
            self.game_state.board[from_coords[1]][from_coords[0]] = 0


            if isinstance(self.game_state.board[to_coords[1]][to_coords[0]], figures.Tower):
                if from_coords[0] == 7:
                    self.game_state.current_player.is_able_rokir_by_right = False
                if from_coords[0] == 0:
                    self.game_state.current_player.is_able_rokir_by_left = False

            if isinstance(self.game_state.board[to_coords[1]][to_coords[0]], figures.King):
                self.game_state.current_player.king_coords = to_coords
                self.game_state.current_player.is_able_rokir_by_left = \
                    self.game_state.current_player.is_able_rokir_by_right = False

                if abs(from_coords[0] - to_coords[0]) > 1: #Если мы рокировались, то:
                    if to_coords[0] == 1:         #Передвигаем ладью вместе с королем
                        tower_to_x = 2
                        tower_from_x = 0
                    else:
                        tower_to_x = 4
                        tower_from_x = 7
                    tower_to_y = to_coords[1]
                    tower_from_y = tower_to_y

                    self.game_state.board[tower_to_y][tower_to_x] = self.game_state.board[tower_from_y][tower_from_x]
                    self.game_state.board[tower_from_y][tower_from_x] = 0
                    self.render.update_board((tower_from_x, tower_from_y), self.game_state.board)
                    self.render.update_board((tower_to_x, tower_to_y), self.game_state.board)

            if isinstance(self.game_state.board[to_coords[1]][to_coords[0]], figures.Pawn): #Убираем пешку, взятую на проходе
                if not isinstance(self.game_state.board[to_coords[1]][to_coords[0]], figures.Figure):
                    # ... - game_state...ID - ID позволяет решить, -1 или +1 нам надо
                    self.game_state.board[to_coords[1] - self.game_state.board[to_coords[1]][to_coords[0]].ID][to_coords[0]] = 0
                    self.render.update_board((to_coords[0], to_coords[1] - \
                        self.game_state.board[to_coords[1]][to_coords[0]].ID), self.game_state.board)

            #Проходная пешка:
            if isinstance(self.game_state.board[to_coords[1]][to_coords[0]], figures.Pawn) and \
               (to_coords[1] == 0 or to_coords[1] == 7):
                    self.game_state.board[to_coords[1]][to_coords[0]] = figures.Queen(BLACK) \
                        if to_coords[1] == 0 else figures.Queen(WHITE)

            self.game_state.last_move = temp_move
            self.game_state.change_player()

            self.render.update_board(from_coords, self.game_state.board)
            self.render.update_board(to_coords, self.game_state.board)



    def get_move(self):
        """
        Возвращает корректный ход (попутно рисует рамку - неисправлено)
        """
        if self.game_state.current_player.is_bot == False:
            while True:
                
                from_coords = self.render.get_coords_by_click()
                take_figure = self.game_state.board[from_coords[1]][from_coords[0]]

                if take_figure == 0:
                    continue

                if self.game_state.current_player.team == WHITE and \
                    take_figure.color == BLACK:
                    continue;

                if self.game_state.current_player.team == BLACK and \
                    take_figure.color == WHITE:
                    continue


                self.render.draw_frame(from_coords)
                to_coords = self.render.get_coords_by_click()
                self.render.update_board(from_coords, self.game_state.board)

                temp_move = (from_coords, to_coords)
                if Game.check_move(temp_move, self.game_state):
                    if not Game.check_under_shah(temp_move, self.game_state):   #check_under_shah не помещен в check_move для оптимизации
                        return temp_move
        else:   
            return robot.Robot.get_move(self.game_state)

    @staticmethod
    def check_move(temp_move, game_state):
        """
        Проверяет коректность хода (за исключением проверки на шах)
        """
        board = game_state.board
        f0 = temp_move[0][0]
        f1 = temp_move[0][1]
        t0 = temp_move[1][0]
        t1 = temp_move[1][1]
        figure = board[f1][f0]

        if board[f1][f0] == 0:
            return False

        if game_state.current_player.team != board[f1][f0].color:
            return False

        if board[t1][t0] != 0 and board[f1][f0].color == board[t1][t0].color:
            return False

        if f0 == t0 and f1 == t1:
            return False
        
        if figure == 0:
            return False

        if isinstance(figure, figures.Pawn):
            return Game.check_move_pawn(f0, f1, t0, t1, game_state)

        if isinstance(figure, figures.Horse):
            return Game.check_move_horse(f0, f1, t0, t1)

        if isinstance(figure, figures.Elf):
            return Game.check_move_elf(f0, f1, t0, t1, board)

        if isinstance(figure, figures.Tower):
            return Game.check_move_tower(f0, f1, t0, t1, board)

        if isinstance(figure, figures.Queen):
            return Game.check_move_elf(f0, f1, t0, t1, board) or Game.check_move_tower(f0, f1, t0, t1, board)

        if isinstance(figure, figures.King):
            if Game.check_move_king(f0, f1, t0, t1, game_state):
                return True


    @staticmethod
    def check_move_pawn(f0, f1, t0, t1, game_state):  # Взятие на проходе отсутствует
        """
        Проверяет корректность хода пешки:
        1) Простой ход вперед
        2) Рубка
        3) Ход вперед через клетку за белых
        4) Ход вперед через клетку за черных
        5) Взятие на проходе за белых
        6) Взятие на проходе за черных
        """
        board = game_state.board
        figure = board[f1][f0].ID       

        if f0 == t0 and f1 + figure == t1 and not isinstance(board[t1][t0], figures.Figure):
            return True
        elif f1 + figure == t1 and abs(t0 - f0) == 1 and isinstance(board[t1][t0], figures.Figure):
            return True
        elif board[f1][f0].color == WHITE and f1 == 1 and t0 == f0 and \
            t1 == 3 and not isinstance(board[2][t0], figures.Figure) and \
            not isinstance(board[3][t0], figures.Figure):
            return True
        elif board[f1][f0].color == BLACK and f1 == 6 and t0 == f0 and \
            t1 == 4 and not isinstance(board[5][t0], figures.Figure) and\
            not isinstance(board[4][t0], figures.Figure):
            return True
        elif board[f1][f0].color == WHITE and f1 == 4 and t1 == 5 and \
            abs(f0 - t0) == 1 and game_state.last_move == ((t0, 6), (t0, 4)):
            return True
        elif board[f1][f0].color == BLACK and f1 == 3 and t1 == 2 and \
            abs(f0 - t0) == 1 and game_state.last_move == ((t0, 1), (t0, 3)):
            return True
        return False

    @staticmethod
    def check_move_horse(f0, f1, t0, t1):
        """
        Проверяет корректность хода коня
        """
        if (abs(t0 - f0) == 1 and abs(t1 - f1) == 2) or (abs(t0 - f0) == 2 and abs(t1 - f1) == 1):
            return True
        return False

    @staticmethod
    def check_move_elf(f0, f1, t0, t1, board):
        """
        Проверяет корректность хода эльфа
        """
        if abs(t0-f0) == abs(t1 - f1):
            if Game.empty_way(f0, f1, t0, t1, board):
                return True
        return False

    @staticmethod
    def check_move_tower(f0, f1, t0, t1, board):
        """
        Проверяет корректность хода ладьи
        """
        if f0 == t0 or f1 == t1:
            if Game.empty_way(f0, f1, t0, t1, board):
                return True
        return False

    @staticmethod
    def check_move_king(f0, f1, t0, t1, game_state):
        """
        Проверяет корректность хода короля
        """
        if isinstance(game_state.board[t1][t0], figures.Figure):
            return False

        if abs(t0-f0) <= 1 and abs(t1-f1) <= 1:
            return True
        elif f1 == t1 and Game.empty_way(f0, f1, t0, t1, game_state.board):
            if t0 == 5 and game_state.current_player.is_able_rokir_by_right:
               return True
            elif t0 == 1 and game_state.current_player.is_able_rokir_by_left:
                return True
            else:
                return False
        return False

    @staticmethod
    def empty_way(f0, f1, t0, t1, board):
        """
        Проверяет, являются ли все клетки от (f0, f1) до (t0, t1) пустыми. Конечные клетки не считаются.
        Траектория вычисляется автоматически, чтобы не делать отдельные empty_way_tower и empty_way_elf
        """
        step_x = int(abs(t0-f0)/(t0-f0)) if not (t0-f0 == 0) else 0
        step_y = int(abs(t1-f1)/(t1-f1)) if not (t1-f1 == 0) else 0
        i = f0 + step_x
        j = f1 + step_y
        while not (i == t0 and j == t1):
            if isinstance(board[j][i], figures.Figure):
                return False    
            i += step_x
            j += step_y     
        return True

    @staticmethod
    def check_under_shah(coords_move, game_state):
        """
        Проверяет, будет ли находиться король текущего игрока под ударом после хода (долга)
        """
        f0 = coords_move[0][0]
        f1 = coords_move[0][1]
        t0 = coords_move[1][0]
        t1 = coords_move[1][1]
        old_board = deepcopy(game_state.board)
        game_state.board[t1][t0] = game_state.board[f1][f0]
        game_state.board[f1][f0] = 0

        if isinstance(game_state.board[t1][t0], figures.King):
            coords_king = (t0, t1)
        else:
            coords_king = game_state.current_player.king_coords
        game_state.current_player.team = WHITE if game_state.current_player.team == BLACK else BLACK
        
        for i in range(0, 8, 1):
            for j in range(0, 8 ,1):
                if game_state.board[j][i] == 0 or game_state.board[j][i].color != game_state.current_player.team: continue
                if Game.check_move(((i, j), coords_king), game_state):
                    game_state.current_player.team = WHITE if game_state.current_player.team == BLACK else BLACK
                    game_state.board = old_board
                    return True
        game_state.current_player.team = WHITE if game_state.current_player.team == BLACK else BLACK
        game_state.board = old_board
        return False

    @staticmethod
    def check_stalemat(game_state):
        """
        Проверяет на наличие мат текущему игроку (очень долга)
        """
        for i in range(0, 8, 1):
            for j in range(0, 8, 1):
                for k in range(0, 8, 1):
                    for l in range(0, 8, 1):
                        if Game.check_move(((i, j), (k, l)), game_state):
                            if not Game.check_under_shah(((i, j), (k, l)), game_state):
                                return False
        return True

    @staticmethod
    def end_game():
        """
        Заканчивает игру (не сделано)
        """
        exit()