from collections import defaultdict
import numpy as np
from tqdm import tqdm


def apply_fft(number_list, start=0):
    length = number_list.shape[0]
    number_list = np.insert(number_list, 0, 0)
    pattern = np.array([0, 1, 0, -1])
    result = []
    for i in tqdm(range(start, length + start)):
        nb_tile = ((start + length) // ((i + 1) * pattern.shape[0])) + 1
        result.append((number_list * np.tile(np.repeat(pattern, i + 1), nb_tile)[start:][:length + 1]).sum())
    result = np.asarray(result)
    return abs(result) % 10


if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    number_list = np.array([int(s) for s in inputs])

    # for i in (range(100)):
    #     number_list = apply_fft(number_list)
    # print(number_list.flatten().tolist())

    number_list = np.tile(number_list, 10000)
    l = (number_list[:7] * (10 ** np.arange(7))[::-1]).sum()
    number_list = number_list[l:]
    for i in range(100):
        number_list = abs(number_list[::-1].cumsum()[::-1]) % 10 # Dirty.
    print(number_list[:8])
