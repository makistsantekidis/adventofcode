import numpy as np
from collections import deque, defaultdict

np.set_printoptions(linewidth=1000, threshold=10000)

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
        uniques = np.unique(self.maze)
        self.keys = [chr(x) for x in range(ord('a'), ord('z') + 1) if chr(x) in uniques]
        self.doors = [chr(x) for x in range(ord('A'), ord('Z') + 1) if chr(x) in uniques]
        self.min_complete_dist = 137
        self.saved_dists = {}

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

    def get_current_distance_matrix(self, starting_point):
        heads = deque([starting_point])
        distances = {heads[0]: 0}
        while len(heads) > 0:
            cur_idx = heads.popleft()
            surround_idxs = surrounding + cur_idx
            for sidx in surround_idxs:
                sidx = tuple(sidx)
                ssymbol = maze[sidx[0], sidx[1]]
                if ssymbol != '#' and sidx not in distances:
                    distances[sidx] = distances[cur_idx] + 1
                    heads.append(sidx)
        return distances

    def construct_dist_matrix(self):
        self.key_dist_dict = dict()
        for k in self.keys:
            self.key_dist_dict[k] = dict()
            kidx = tuple(np.argwhere(maze == k)[0])
            distance_matrix = self.get_current_distance_matrix(kidx)
            for k2 in set(self.keys) - set([k]):
                self.key_dist_dict[k][k2] = distance_matrix[tuple(np.argwhere(maze == k2)[0])]
        return self.key_dist_dict

    def get_max_dist(self, missing_keys):
        max_dist = -np.inf
        for k in missing_keys:
            for k2 in set(missing_keys) - set([k]):
                max_dist = max(self.key_dist_dict[k][k2], max_dist)
        return max_dist

    def key_distances(self, starting_point, current_distance=0, obt_keys=[]):
        heads = deque([starting_point])
        distances = {heads[0]: 0}
        # obstacles = defaultdict(list)
        # obstacles[heads[0]] = []
        missing_keys = set(self.keys) - set(obt_keys)
        # print(obt_keys)
        if missing_keys == set():
            if self.min_complete_dist > current_distance:
                self.min_complete_dist = current_distance
                print(current_distance)
            return current_distance
        elif self.get_max_dist(missing_keys) + current_distance >= self.min_complete_dist:
            return None
        while len(heads) > 0:
            cur_idx = heads.popleft()
            surround_idxs = surrounding + cur_idx
            for sidx in surround_idxs:
                sidx = tuple(sidx)
                ssymbol = maze[sidx[0], sidx[1]]
                if ssymbol != '#' and sidx not in distances:
                    distances[sidx] = distances[cur_idx] + 1
                    if distances[sidx] + current_distance > self.min_complete_dist:
                        continue
                    # obstacles[sidx].extend(obstacles[cur_idx])
                    if (ssymbol in self.doors) and (ssymbol.lower() in missing_keys):
                        continue
                        # obstacles[sidx].append(ssymbol.lower())
                    if ssymbol in missing_keys:
                        continue
                    heads.append(sidx)
        # distance_matrix = maze.copy()
        # for k, v in distances.items():
        #     distance_matrix[k[0], k[1]] = v

        key_dists = dict()

        ks = []
        for k in missing_keys:
            kidx = tuple(np.argwhere(maze == k)[0])
            if kidx in distances:
                dst = distances[kidx]
                ks.append((k, dst))
        sks = [k[0] for k in sorted(ks, key=lambda x: x[1])]

        for k in sks:
            kidx = tuple(np.argwhere(maze == k)[0])
            if kidx in distances:
                dst = distances[kidx] + current_distance
                if dst >= self.min_complete_dist:
                    continue
                new_dst = self.key_distances(kidx, dst, obt_keys + [k])
                if new_dst is not None:
                    key_dists[k] = new_dst
        if len(key_dists) > 0:
            return min(list(key_dists.values()))
        else:
            return None


if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    maze = np.array([list(l) for l in inputs.splitlines()])
    mz = MazeSolver(maze)
    print(mz.construct_dist_matrix())
    center = tuple(np.argwhere(maze == '@')[0])
    print(mz.keys)
    print(mz.key_distances(center))
