import numpy as np

if __name__ == '__main__':
    matrix = np.asarray([list(l) for l in open('inputs.txt').read().splitlines()])
    locations = np.argwhere(matrix == '#')
    # obs_list = []
    # for i, cand in enumerate(locations):
    #     lcopy = np.delete(locations.copy(), i, axis=0)
    #     diffs = cand - lcopy
    #     nb_observables = 0
    #     while len(diffs) > 0:
    #         for i in range(len(diffs)):
    #             cdiff = diffs[i]
    #             cdiff = (cdiff // abs(np.gcd(cdiff[0], cdiff[1])))
    #             shadow_idxs = ((diffs % cdiff) == 0) & (np.sign(cdiff) == np.sign(diffs))
    #             frac = (diffs // cdiff)
    #             shadow_idxs = shadow_idxs.all(axis=1) & ((frac[:, 0] == frac[:, 1]) |  ((frac == 0).any(axis=1)))
    #             nb_observables += 1
    #             diffs = np.delete(diffs, np.argwhere(shadow_idxs).flatten(), axis=0)
    #             if i + 1 >= len(diffs):
    #                 break
    #     obs_list.append(nb_observables)

    # m2 = np.argwhere(np.ones(matrix.shape))
    # m2 = m2 - 16
    # rads = np.arctan2(m2[:, 1], m2[:, 0]).reshape(matrix.shape)

    # for i, cand in enumerate(locations):
    #     lcopy = np.delete(locations.copy(), i, axis=0)
    #     diffs = cand - lcopy
    #     fracz = diffs[:, 1] / diffs[:, 0]
    #     sdiffs = np.sign(diffs)
    #     nb_observables = 0
    #     while len(diffs) > 0:
    #         shadow_idxs = (fracz == fracz[0]) & ((sdiffs[0] == sdiffs).all(axis=1))
    #         diffs = diffs[~shadow_idxs]
    #         fracz = fracz[~shadow_idxs]
    #         nb_observables += 1
    #     obs_list.append(nb_observables)
    # print(max(obs_list))
    observable_counts = []
    for i, candidate in enumerate(locations):
        diffs = candidate - locations
        diffs //= np.gcd(*diffs.T)[:, np.newaxis]
        observable_counts.append(len(np.unique(diffs, axis=0)))
    print(max(observable_counts) - 1)

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
