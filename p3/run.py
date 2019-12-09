import numpy as np
import plotly.graph_objects as go

move_dict = dict(
    U=np.array((0, 1)),
    D=np.array((0, -1)),
    R=np.array((1, 0)),
    L=np.array((-1, 0)),
)


def generate_points(path):
    cur_pos = np.array((0, 0))
    point_trail = [cur_pos]
    dists = [0]
    for m in path:
        step_size = int(m[1:])
        cur_pos = move_dict[m[:1]] * step_size + cur_pos
        dists.append(step_size + dists[-1])
        point_trail.append(cur_pos)
    return point_trail, dists


def is_horizontal(a, b):
    return a[..., 1] == b[..., 1]


def do_intersect(hza, hzb, vta, vtb):
    hzmin, hzmax = min(hza[0], hzb[0]), max(hza[0], hzb[0])
    vtmin, vtmax = min(vta[1], vtb[1]), max(vta[1], vtb[1])
    return hzmax > vta[0] > hzmin and vtmax > hza[1] > vtmin


if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()

    path1, path2 = inputs.splitlines(keepends=False)
    path1 = path1.split(',')
    path2 = path2.split(',')

    pl1, dst1 = generate_points(path1)
    pl2, dst2 = generate_points(path2)
    pl1 = np.stack(pl1)
    pl2 = np.stack(pl2)

    # fig = go.Figure()
    # fig.add_scattergl(x=pl1[:, 0], y=pl1[:, 1], name='path1')
    # fig.add_scattergl(x=pl2[:, 0], y=pl2[:, 1], name='path2')
    # fig.show()
    distsum = []
    for i in range(1, pl1.shape[0]):
        ishz1 = is_horizontal(pl1[i - 1], pl1[i])
        for j in range(1, pl2.shape[0]):
            if ishz1 == is_horizontal(pl2[j - 1], pl2[j]):
                continue
            if ishz1:
                did_intersect = do_intersect(pl1[i - 1], pl1[i], pl2[j], pl2[j - 1])
            else:
                did_intersect = do_intersect(pl2[j], pl2[j - 1], pl1[i - 1], pl1[i])
            if did_intersect:
                if ishz1:
                    intrsx = np.array((pl2[j, 0], pl1[i, 1]))
                else:
                    intrsx = np.array((pl1[i, 0], pl2[j, 1]))
                cur_dist = dst1[i - 1] + dst2[j - 1]
                extra_dist = np.abs(intrsx - pl1[i - 1]).sum() + np.abs(intrsx - pl2[j - 1]).sum()
                distsum.append(cur_dist+extra_dist)
    print(min(distsum))
