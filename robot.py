import gamestate
import game
import random
import time
import figures


class Robot():

    @staticmethod
    def get_move(game_state):
        if game_state.current_player.level == 0:
            return Robot.get_random_move(game_state)
        elif game_state.current_player.level == 1:
            return Robot.get_best_move(game_state)
        else:
            pass

    @staticmethod
    def get_random_move(game_state):
         while True:
            i = random.randrange(0, 8, 1)
            j = random.randrange(0, 8, 1)
            k = random.randrange(0, 8, 1)
            l = random.randrange(0, 8, 1)

            if game.Game.check_move(((i, j), (k, l)), game_state):
                if not game.Game.check_stalemat(game_state):
                    if not game.Game.check_under_shah(((i, j), (k, l)), game_state):
                        return ((i, j), (k, l))
                else:
                    print("I lost :C")
                    game.Game.end_game();

    @staticmethod
    def get_best_move(game_state):
        """
        Смотрит самый выгодный ход (продумывает на один полуход)
        """
        max_cost = -100500
        best_move = tuple()
        for i in range(0, 8, 1):
            for j in range(0, 8, 1):
                for k in range(0, 8, 1):
                    for l in range(0, 8, 1):
                        if i == 5 and j == 6 and k == 6 and l == 5:
                            pass
                        if game_state.board[l][k] == 0 and max_cost > 0: continue
                        if isinstance(game_state.board[l][k], figures.Figure) and game_state.board[l][k].cost < max_cost: continue
                        if game.Game.check_move(((i, j), (k, l)), game_state):
                            if not game.Game.check_stalemat(game_state):
                                if not game.Game.check_under_shah(((i, j), (k, l)), game_state):
                                    max_cost = 0 if not isinstance(game_state.board[l][k], figures.Figure) \
                                        else game_state.board[l][k].cost
                                    best_move = ((i, j), (k, l))
                            else:
                                print("I lost :C")
                                game.Game.end_game();
        return best_move