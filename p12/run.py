import numpy as np
import numba as nb
from tqdm import tqdm


@nb.njit
def simulate_till_initial_state(initial_state):
    points = initial_state.copy()
    velocities = np.zeros_like(points)
    i = 0
    for i in (range(100_000_000_000)):
        velocities += np.sum(points.reshape(4, 3, 1) < points.T, axis=2) \
                      - np.sum(points.reshape(4, 3, 1) > points.T, axis=2)
        points += velocities
        if (i % 10_000_000) == 0:
            print('.')
        if (points[0] == initial_state[0]).all():
            if (points[1] == initial_state[1]).all():
                if (points[2] == initial_state[2]).all():
                    if (points[3] == initial_state[3]).all():
                        break
    return i


if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    points = [l[1:-1].replace(' ', '').split(',') for l in inputs.splitlines()]
    for i in range(len(points)):
        for j in range(len(points[i])):
            points[i][j] = int(points[i][j].split('=')[1])
    points = np.array(points)
    initial_state = points
    velocities = np.zeros_like(points)
    # for i in range(1000):
    #     acceleration = -np.count_nonzero(points[..., np.newaxis] > points.T, axis=2)
    #     acceleration += np.count_nonzero(points[..., np.newaxis] < points.T, axis=2)
    #     velocities += acceleration
    #     points += velocities
    #     # if ((i + 1) % 10) == 0:
    #     #     print(i, points)
    # potential = np.abs(points).sum(axis=1)
    # kinetic = np.abs(velocities).sum(axis=1)
    # total = (potential * kinetic).sum()
    # print(total)
    print(simulate_till_initial_state(initial_state))
