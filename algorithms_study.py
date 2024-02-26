from minmax import minimax
from minimax_prunning import minimax_pruning
import pandas as pd
import numpy as np
from time import time
from memory_profiler import memory_usage
import tqdm


def time_fn(fn, **kwargs):
    start = time()
    fn(**kwargs)
    return time() - start


def track_memory(fn, **kwargs):
    mem_usage = memory_usage((fn, (), kwargs))
    return max(mem_usage) - min(mem_usage)


def generate_initial_state():
    values = np.random.choice(range(25), size=6, replace=False).astype(np.int64)
    white, black = set(values[:3]), set(values[3:])
    player = np.random.choice(['Black', 'White'])
    return white, black, player


if __name__ == '__main__':
    max_depth = 9
    start_depth = 1
    length = max_depth - start_depth + 1
    num_reps = 5
    names = [f'Depth{i}' for i in range(start_depth, max_depth + 1)]
    data = {'minimaxTime': [0] * length, 'minimaxPruningTime': [0] * length,
            'minimaxMemory': [0] * length, 'minimaxPruningMemory': [0] * length}

    init = [generate_initial_state() for _ in range(num_reps)]

    for depth in range(start_depth, max_depth+1):
        if depth <= 7:
            time_minimax = [time_fn(minimax, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
            mem_minimax = [track_memory(minimax, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
        else:
            time_minimax = [-1]
            mem_minimax = [-1]
        time_minimax_pruning = [time_fn(minimax_pruning, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]
        mem_minimax_pruning = [track_memory(minimax_pruning, white=white, black=black, player=player, depth=depth) for white, black, player in tqdm.tqdm(init)]

        data['minimaxTime'][depth-1] = np.mean(time_minimax)
        data['minimaxPruningTime'][depth-1] = np.mean(time_minimax_pruning)
        data['minimaxMemory'][depth-1] = np.mean(mem_minimax)
        data['minimaxPruningMemory'][depth-1] = np.mean(mem_minimax_pruning)

    df = pd.DataFrame(data, index=names)
    from IPython import embed
    embed()


