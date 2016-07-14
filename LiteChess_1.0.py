import game
import sys
import player


WHITE = 0
BLACK = 1

#Игроки задаются в аргументами (bot0, bot1, human)

try:
    if sys.argv[1] == "bot0":
        player1 = player.Player(True, WHITE, 0)
    elif sys.argv[1] == "bot1":
        player1 = player.Player(True, WHITE, 1)
    else:
        player1 = player.Player(False, WHITE)
except IndexError:
    player1 = player.Player(False, WHITE)

try:
    if sys.argv[2] == "bot0":
        player2 = player.Player(True, BLACK, 0)
    elif sys.argv[2] == "bot1":
        player2 = player.Player(True, BLACK, 1)
    else:
        player2 = player.Player(False, BLACK)
except:
    player2 = player.Player(False, BLACK)

new_game = game.Game(player1, player2)
new_game.play()
