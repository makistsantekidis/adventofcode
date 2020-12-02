import numpy as np

if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    points = [l[1:-1].replace(' ', '').split(',') for l in inputs.splitlines()]
    for i in range(len(points)):
        for j in range(len(points[i])):
            points[i][j] = int(points[i][j].split('=')[1])
    points = np.array(points)
    initial_state = points.copy()
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
    reset_step = np.zeros(3, dtype=np.int)
    i = 1
    while (reset_step == 0).any():
        acceleration = -np.count_nonzero(points[..., np.newaxis] > points.T, axis=2)
        acceleration += np.count_nonzero(points[..., np.newaxis] < points.T, axis=2)
        velocities += acceleration
        points += velocities
        reset_step[((points == initial_state) & (velocities == 0)).all(axis=0) & (reset_step == 0)] = i
        i += 1
    print(reset_step)
    lcm = np.lcm.reduce(reset_step)
    print(lcm)
