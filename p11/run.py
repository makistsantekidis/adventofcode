import numpy as np
from intcode import IntCodeComputer
from collections import defaultdict

moves = {
    0: lambda x: (np.array((1, -1)) * x)[::-1],
    1: lambda x: (np.array((-1, 1)) * x)[::-1]
}

if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    program = [int(i) for i in inputs.split(',')]
    panel_colors = defaultdict(lambda: 0)
    panel_colors[(0, 0)] = 1
    computer = IntCodeComputer(inputs, inputs=[], interactive=True)
    position = np.array((0, 0))
    direction = np.array((0, 1))
    output_list = []
    while not computer.done:
        output = computer.run()
        if output == '_':
            computer.inputs.append(panel_colors[tuple(position)])
        elif isinstance(output, int):
            output_list.append(output)
        else:
            # raise ValueError("Unknown output")
            print(output)
        if len(output_list) == 2:
            panel_colors[tuple(position)] = output_list[0]
            direction = moves[output_list[1]](direction)
            position += direction
            output_list = []
    print(len(panel_colors))

    parray = np.array(list(panel_colors.keys()))
    pmax, pmin = parray.max(), parray.min()
    msize = pmax - pmin + 1
    painted = np.zeros((msize, msize))
    amin = abs(pmin)
    for k, v in panel_colors.items():
        painted[amin + k[0], amin + k[1]] = v
    print(painted)
