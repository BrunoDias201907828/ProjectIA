import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import functools
from algorithms.minmax import minimax
from algorithms.alpha_beta import minimax_pruning
from algorithms.alpha_beta import minimax_pruning as minimax_no_cutoff
import pandas as pd
import numpy as np
from time import time
import tracemalloc
import tqdm
from algorithms.heuristics import eval_no_heuristic
from algorithms.alpha_beta_cutoff import alpha_beta_cutoff
from algorithms.monte_carlo import mcts


def time_fn(fn, **kwargs):
    start = time()
    fn(**kwargs)
    return time() - start


def track_memory(fn, **kwargs):
    tracemalloc.clear_traces()
    fn(**kwargs)
    first_size, first_peak = tracemalloc.get_traced_memory()
    return first_peak


def generate_initial_state():
    values = np.random.choice(range(25), size=6, replace=False).astype(np.int64)
    white, black = set(values[:3]), set(values[3:])
    player = np.random.choice(['Black', 'White'])
    return white, black, player


def mixmax_vs_alphabeta():
    max_depth = 9
    start_depth = 3
    length = max_depth - start_depth + 1
    num_reps = 5
    names = [f'Depth{i}' for i in range(start_depth, max_depth + 1)]
    data = {'minimaxTime': [0] * length, 'minimaxPruningTime': [0] * length,
            'minimaxMemory': [0] * length, 'minimaxPruningMemory': [0] * length}

    init = [generate_initial_state() for _ in range(num_reps)]

    for i, depth in enumerate(range(start_depth, max_depth+1)):
        if depth <= 7:
            # time_minimax = [time_fn(minimax, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
            time_minimax = [-1]
            tracemalloc.start()
            mem_minimax = [track_memory(minimax, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
            tracemalloc.stop()
        else:
            time_minimax = [-1]
            mem_minimax = [-1]
        # time_minimax_pruning = [time_fn(minimax_pruning, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
        time_minimax_pruning = [-1]
        tracemalloc.start()
        mem_minimax_pruning = [track_memory(minimax_pruning, white=white, black=black, player=player, depth=depth, heuristic=eval_no_heuristic) for white, black, player in tqdm.tqdm(init)]
        tracemalloc.stop()

        data['minimaxTime'][i] = np.mean(time_minimax)
        data['minimaxPruningTime'][i] = np.mean(time_minimax_pruning)
        data['minimaxMemory'][i] = np.mean(mem_minimax)
        data['minimaxPruningMemory'][i] = np.mean(mem_minimax_pruning)
    df = pd.DataFrame(data, index=names)
    df.to_csv('minmax.csv')
    from IPython import embed
    embed()


def heuristics():
    max_depth = 9
    start_depth = 3
    length = max_depth - start_depth + 1
    num_reps = 5
    names = [f'Depth{i}' for i in range(start_depth, max_depth + 1)]
    data = {
        'noCutoffTime'  : [0] * length, 'CutoffTime'  : [0] * length,
        'noCutoffMemory': [0] * length, 'CutoffMemory': [0] * length
    }
    no_cutoff = functools.partial(minimax_no_cutoff, heuristic=eval_no_heuristic)
    cutoff = functools.partial(alpha_beta_cutoff, heuristic=eval_no_heuristic)

    init = [generate_initial_state() for _ in range(num_reps)]

    for i, depth in enumerate(range(start_depth, max_depth+1)):
        print(i)
        time_no_cutoff = [time_fn(no_cutoff, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
        tracemalloc.start()
        mem_no_cutoff = [track_memory(no_cutoff, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
        tracemalloc.stop()

        time_cutoff = [time_fn(cutoff, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
        tracemalloc.start()
        mem_cutoff = [track_memory(cutoff, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
        tracemalloc.stop()

        data['noCutoffTime'][i] = np.mean(time_no_cutoff)
        data['noCutoffMemory'][i] = np.mean(mem_no_cutoff)
        data['CutoffTime'][i] = np.mean(time_cutoff)
        data['CutoffMemory'][i] = np.mean(mem_cutoff)
    df = pd.DataFrame(data, index=names)
    df.to_csv('heuristics.csv')
    from IPython import embed
    embed()


def monte_carlo():
    times_limits = [30, 60, 120]
    num_reps = 5
    names = [f'Time{i}' for i in times_limits]
    length = len(times_limits)
    data = {
        'n_visits'  : [0] * length, 'memory'  : [0] * length
    }
    init = [generate_initial_state() for _ in range(num_reps)]

    for i, time_limit in enumerate(times_limits):
        visits = [mcts(white=white, black=black, player=player, time_limit=time_limit)[0] for white, black, player in tqdm.tqdm(init)]
        tracemalloc.start()
        mem = [track_memory(mcts, white=white, black=black, player=player, time_limit=time_limit) for white, black, player in tqdm.tqdm(init)]
        tracemalloc.stop()
        data['n_visits'][i] = np.mean(visits)
        data['memory'][i] = np.mean(mem)
    df = pd.DataFrame(data, index=names)
    df.to_csv('mcts.csv')


if __name__ == '__main__':
    # mixmax_vs_alphabeta()
    # heuristics()
    monte_carlo()


