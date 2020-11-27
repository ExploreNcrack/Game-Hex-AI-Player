from AIPlayer import *

experiment_board_size = 5 

num_runs = 10

ai_player = AIPlayer()

random_player_win_count = 0
strategy_player_win_count = 0
simulation_player_win_count = 0

print("\nRandom player plays first against greedy strategy player")
# random player plays first against greedy strategy player
for i in range(num_runs):
    board = [[0 for _ in range(experiment_board_size)] for __ in range(experiment_board_size)]    
    current_player_color = 1 # first
    result = -1
    while True:
        # random player move
        random_player_move = ai_player.random_player(board)
        board[random_player_move[0]][random_player_move[1]] = current_player_color
        result = ai_player.check_win(board)
        if result != 0:
            break
        current_player_color = 3 - current_player_color  # switch turn

        # strategy player move
        strategy_move = ai_player.strategy_move(board, current_player_color)
        board[strategy_move[0]][strategy_move[1]] = current_player_color
        result = ai_player.check_win(board)
        if result != 0:
            break
        current_player_color = 3 - current_player_color  # switch turn

    if result == 1:
        random_player_win_count += 1
        print("round %s: random player win" % (i+1))
    elif result == 2:
        strategy_player_win_count += 1
        print("round %s: 'greedy' strategy player win" % (i+1))

print("Experiment run: %s" % (num_runs))
print("Random player wins: %s"%(random_player_win_count))
print("Strategy player wins: %s"%(strategy_player_win_count))


print("\nSimulation-based player plays first against greedy strategy player")
# simulation-based player plays first against greedy strategy player
simulation_player_win_count = 0
strategy_player_win_count = 0
for i in range(num_runs):
    board = [[0 for _ in range(experiment_board_size)]  for __ in range(experiment_board_size)]
    current_player_color = 1  # first
    result = -1
    while True:
        # simulation-based player move
        random_player_move = ai_player.gen_move_by_simulation_based_strategy(board, current_player_color)
        board[random_player_move[0]][random_player_move[1]] = current_player_color
        result = ai_player.check_win(board)
        if result != 0:
            break
        current_player_color = 3 - current_player_color  # switch turn

        # strategy player move
        strategy_move = ai_player.strategy_move(board, current_player_color)
        board[strategy_move[0]][strategy_move[1]] = current_player_color
        result = ai_player.check_win(board)
        if result != 0:
            break
        current_player_color = 3 - current_player_color  # switch turn

    if result == 1:
        simulation_player_win_count += 1
        print("round %s: simulation-based player win" % (i+1))
    elif result == 2:
        strategy_player_win_count += 1
        print("round %s: 'greedy' strategy player win" % (i+1))

print("Experiment run: %s" % (num_runs))
print("Simulation-based player wins: %s" % (simulation_player_win_count))
print("Strategy player wins: %s" % (strategy_player_win_count))

print("\nGreedy strategy player plays first against simulation-based strategy player")
# simulation-based player plays first against greedy strategy player
simulation_player_win_count = 0
strategy_player_win_count = 0
for i in range(num_runs):
    board = [[0 for _ in range(experiment_board_size)]  for __ in range(experiment_board_size)]
    current_player_color = 1  # first
    result = -1
    while True:
        # strategy player move
        strategy_move = ai_player.strategy_move(board, current_player_color)
        board[strategy_move[0]][strategy_move[1]] = current_player_color
        result = ai_player.check_win(board)
        if result != 0:
            break
        current_player_color = 3 - current_player_color  # switch turn

        # simulation-based player move
        random_player_move = ai_player.gen_move_by_simulation_based_strategy(board, current_player_color)
        board[random_player_move[0]][random_player_move[1]] = current_player_color
        result = ai_player.check_win(board)
        if result != 0:
            break
        current_player_color = 3 - current_player_color  # switch turn

    if result == 2:
        simulation_player_win_count += 1
        print("round %s: simulation-based player win" % (i+1))
    elif result == 1:
        strategy_player_win_count += 1
        print("round %s: 'greedy' strategy player win" % (i+1))
print("\nExperiment run: %s" % (num_runs))
print("Strategy player wins: %s" % (strategy_player_win_count))
print("Simulation-based player wins: %s" % (simulation_player_win_count))
