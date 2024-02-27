from minmax import minimax, eval_no_heuristic, eval_mobility, eval_alignment, eval_mobility_alignment
#from minimax_prunning import minimax_pruning
from last_prunning import minimax_pruning
from utils import is_winner
import typing as ty
import numpy as np
import tqdm
import functools


def is_draw(white: set, black: set, played_moves: dict):
    key = (frozenset(white), frozenset(black))
    return played_moves.get(key, 0) >= 3


def game_simulation(algorithm1: ty.Callable, algorithm2: ty.Callable, start_player: int):
    algorithm_dict = {1: algorithm1, 2: algorithm2}
    white, black = {1, 3, 17}, {7, 21, 23}
    played_moves = None
    player = start_player
    turn = 'Black'
    n_plays = 0

    while True:
        n_plays += 1
        algorithm_playing = algorithm_dict[player]
        value, move, played_moves = algorithm_playing(white, black, turn, played_moves=played_moves)

        set_to_change = white if turn == 'White' else black
        set_to_change.remove(move[0])
        set_to_change.add(move[1])

        if is_winner(set_to_change):
            return player, n_plays
        elif is_draw(white, black, played_moves):
            return 0, n_plays

        turn = 'Black' if turn == 'White' else 'White'
        player = 1 if player == 2 else 2


def get_statistics_deterministic(algorithm1: ty.Callable, algorithm2: ty.Callable):
    results = {0: 0, 1: 0, 2: 0}
    n_plays = []
    for i in tqdm.tqdm(range(2)):
        start_player = i + 1
        print(start_player)
        winner, plays = game_simulation(algorithm1, algorithm2, start_player)
        results[winner] += 1
        n_plays.append(plays)
    return results, n_plays

def get_statistics(algorithm1: ty.Callable, algorithm2: ty.Callable, n_games: int):
    results = {0: 0, 1: 0, 2: 0}
    n_plays = []
    for _ in tqdm.tqdm(range(n_games)):
        start_player = np.random.choice([1, 2])
        winner, plays = game_simulation(algorithm1, algorithm2, start_player)
        results[winner] += 1
        n_plays.append(plays)
        print(results, n_plays)
    return results, n_plays

minimax_pruning_no_heuristic = functools.partial(minimax_pruning, heuristic=eval_no_heuristic)
minimax_pruning_mobility = functools.partial(minimax_pruning, heuristic=eval_mobility)
minimax_pruning_alignment = functools.partial(minimax_pruning, heuristic=eval_alignment)
minimax_pruning_mobility_alignment = functools.partial(minimax_pruning, heuristic=eval_mobility_alignment)

if __name__ == '__main__':
    #r, np = get_statistics(minimax, minimax_pruning, 50)
    #r, np = get_statistics_deterministic(minimax, minimax_pruning_no_heuristic)
    #r, np = get_statistics_deterministic(minimax_pruning_no_heuristic, minimax_pruning_mobility)
    #r, np = get_statistics_deterministic(minimax_pruning_no_heuristic, minimax_pruning_alignment)
    #r, np = get_statistics_deterministic(minimax_pruning_no_heuristic, minimax_pruning_mobility_alignment)
    #r, np = get_statistics_deterministic(minimax_pruning_mobility, minimax_pruning_alignment)
    #r, np = get_statistics_deterministic(minimax_pruning_mobility, minimax_pruning_mobility_alignment)
    r, np = get_statistics_deterministic(minimax_pruning_alignment, minimax_pruning_mobility_alignment)    
    from IPython import embed
    embed()



