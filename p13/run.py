import numpy as np
from intcode import IntCodeComputer
from collections import defaultdict

if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    program = [int(i) for i in inputs.split(',')]

    outputs = []
    computer = IntCodeComputer(inputs, interactive=True)
    computer.program[0] = 2
    while not computer.done:
        outputs.append(computer.run())
        if outputs[-1] == '_':
            break
    screen = np.array(outputs[:-1]).reshape(-1, 3)
    pixels = np.zeros((screen[:, 0].max() + 1, screen[:, 1].max() + 1))
    pixels[screen[:, 0], screen[:, 1]] = screen[:, 2]
    print(pixels)
    print(np.count_nonzero(pixels == 2))
