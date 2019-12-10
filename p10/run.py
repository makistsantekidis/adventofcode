import numpy as np

if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()
    matrix = [list(l) for l in inputs.splitlines()]
    matrix = np.asarray(matrix)

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
    for i, cand in enumerate(locations):
        diffs = cand - locations
        diffs = diffs // np.gcd(diffs[:, 0], diffs[:, 1]).reshape(-1, 1)
        observable_counts.append(np.unique(diffs, axis=0).shape[0])
    print(max(observable_counts) - 1)

    Nth = 200
    obs_coords = locations[np.argmax(observable_counts)]
    diffs = obs_coords - locations
    distances = np.sqrt((diffs ** 2).sum(axis=1))
    normed_diffs = diffs // np.gcd(diffs[:, 1], diffs[:, 0]).reshape(-1, 1)
    arcs = np.arctan2(normed_diffs[:, 0], normed_diffs[:, 1])
    unique_arcs, arc_counts = np.unique(arcs, return_counts=True)
    rotation_order = np.argsort(unique_arcs)[::-1]
    assert Nth < unique_arcs.shape[0]
    location_candidates = np.argwhere([arcs == unique_arcs[rotation_order[Nth - 1]]]).flatten()
    nth_idx = location_candidates[distances[location_candidates].argmin()]
    print(locations[nth_idx])

# 622 - 2001
