import numpy as np

surrounding = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])


def select_surround(maze, exploration_dict, cur_idx):
    surrounding_idx = cur_idx + surrounding
    dots_idxs = np.argwhere(maze[surrounding_idx[:, 0], surrounding_idx[:, 1]] == '.')
    nb_unexplored = dots_idxs.shape[0]
    for d in dots_idxs:
        didx = surrounding[d]
        if tuple(didx) in exploration_dict:
            nb_unexplored -= 1
        else:
            return didx
    return None


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start_idx = np.argwhere(maze == '@')[0]
        self.cur_idx = self.start_idx
        self.total_dist, cur_dist = 0, 0
        self.exploration_dict = dict()
        self.distance_dict = dict()
        self.visible_keys = dict()

    def select_surround(self):
        surrounding_idx = self.cur_idx + surrounding
        dots_idxs = np.argwhere(self.maze[surrounding_idx[:, 0], surrounding_idx[:, 1]] != '#')
        nb_unexplored = dots_idxs.shape[0]
        selection = None
        for d in dots_idxs:
            didx = surrounding[d[0]]
            if maze[didx[0], didx[1]] not in ['.', '@']:
                self.visible_keys[maze[didx]] = didx
            if tuple(didx) in self.exploration_dict:
                nb_unexplored -= 1
            else:
                selection = didx
        self.exploration_dict[self.cur_idx] = nb_unexplored
        self.cur_dist += 1
        self.distance_dict[self.cur_idx] = self.cur_dist
        self.cur_idx = selection
        return selection

    def select_unexplored(self):
        min_idx = None
        for k, v in self.distance_dict:
            if self.exploration_dict[k] == 0:
                continue
            if min_idx is None:
                min_idx = k
            elif v < self.distance_dict[min_idx]:
                min_idx = k
        self.cur_idx = min_idx
        self.cur_dist = self.distance_dict[min_idx]
        return min_idx

    def solve(self):
        while True:
            if tuple(self.cur_idx) not in self.exploration_dict or \
                    self.exploration_dict[tuple(self.cur_idx)] > 0:
                self.cur_idx = self.select_surround()
            else:
                self.select_unexplored()
            print(self.cur_idx)


if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    maze = np.array([list(l) for l in inputs.splitlines()])
    mz = MazeSolver(maze)
    mz.solve()
