import numpy as np

if __name__ == '__main__':
    matrix = np.asarray([list(l) for l in open('inputs.txt').read().splitlines()])
    locations = np.argwhere(matrix == '#')
    diff_matrix = locations[..., np.newaxis] - locations.T
    diff_matrix //= np.gcd(*diff_matrix.transpose(1, 0, 2))[:, np.newaxis]
    print(max([len(np.unique(diffs.T, axis=0)) for diffs in diff_matrix]) - 1)

    # observable_counts = []
    # for i, candidate in enumerate(locations):
    #     diffs = candidate - locations
    #     diffs //= np.gcd(*diffs.T)[:, np.newaxis]
    #     observable_counts.append(len(np.unique(diffs, axis=0)))
    # print(max(observable_counts) - 1)

    Nth = 200
    station_coords = locations[np.argmax(observable_counts)]
    diffs = locations - station_coords
    distances = np.sqrt((diffs ** 2).sum(axis=1))
    diffs //= np.gcd(*diffs.T)[:, np.newaxis]
    arcs = np.arctan2(*diffs.T[::-1])
    unique_arcs = np.sort(np.unique(arcs))[::-1]
    assert Nth < unique_arcs.shape[0]
    location_candidates = arcs == unique_arcs[Nth - 1]
    nth_coords = locations[location_candidates][distances[location_candidates].argmin()]
    print(nth_coords)

    # render = np.zeros(matrix.shape)
    # render[locations[:, 0], locations[:, 1]] = arcs
    # # for i in range(rotation_order.shape[0]):
    # #     locs = locations[arcs == unique_arcs[rotation_order[i]]]
    # #     render[locs[:,0], locs[:, 1]] = i
    # print(render)

    # 622 - 2001
