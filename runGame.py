import board
import game
import player
import randomPlayer
# Note that you can comment out the following if you don't want to seed the random player differently each run
from datetime import datetime

round = 0
total_expanded = 0
total_pruned = 0
win_rate = 0
while round < 10:
    # This script allows you to test your solution.
    # Your coursework implementation must always be player 1.
    # You should consider changing player 2 to use a minimax approach for evaluation.
    # It is recommended that you also consider other game board sizes, and vary the number of pieces 
    # that are required in a line to win. There are examples of the method calls to create such games
    # commented out below.
    p1 = player.Player("X")

    # Player 2 currently picks random moves and so, while player 2 is not very good, it does allow you to
    # start testing your solution. Once you have something sensible, you should change player 2 to be more 
    # intelligent. Note that you can specify a seed for the random player (currently the seed is '42'),
    # which allows for testing in a consistent environment.
    # Note that the following two lines seed the random player differently each run
    # seed = datetime.now().timestamp()
    # p2 = randomPlayer.RandomPlayer("O", seed)
    # Instead of randomly seeding, you can comment out the following line to seed the random player and
    # test with a consistent opponent
    player_2 = player.Player("O")
    p2 = randomPlayer.SmartPlayer("O",player_2)

    # The arguments to game.Game specify the two players, the number of rows, the number of columns
    # and the number of pieces that need to be placed in a line in order to win.
    # g = game.Game(p1, p2, 7, 7, 6)
    # g = game.Game(p1, p2, 6, 7, 5)
    # g = game.Game(p1, p2, 6, 6, 5)
    # g = game.Game(p1, p2, 5, 6, 4)
    # g = game.Game(p1, p2, 5, 5, 4)
    # g = game.Game(p1, p2, 4, 5, 3)
    # g = game.Game(p1, p2, 4, 4, 3)
    # g = game.Game(p1, p2, 3, 3, 2)

    g = game.Game(p1, p2, 6, 7, 4)

    # You can pass 'True' to the playGame() method to test your alpha-beta pruning approach, i.e., to make
    # player 1 use alpha-beta. If you want player 2 to use alpha-beta you will need to ensure 
    # that you create player 2 accordingly. 
    win_rate += g.playGame(True)
    total_expanded += p1.numExpanded
    total_pruned += p1.numPruned
    
    round += 1

print("=============== Ending stats ===============\n")
print(f"AI won {win_rate} out of {round} rounds!")
print(f"Expanded a total of {total_expanded} and pruned {total_pruned} nodes")