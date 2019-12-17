"""
Please don't look at this. I don't know how this ended up working but it did.
"""

import numpy as np
from intcode import IntCodeComputer
from collections import defaultdict
import time

np.set_printoptions(linewidth=220, threshold=10000)


def coords_to_mem(x, y):
    return x * 38 + y


if __name__ == '__main__':
    inputs = open('inputs.txt').read()
    program = [int(i) for i in inputs.split(',')]

    outputs = []
    computer = IntCodeComputer(inputs, interactive=True)
    mem = computer.program
    mem[0] = 2
    for i in range(1286 - 38, 1322 - 38):
        mem[i] = 1
    # mem[1398] = 2
    # mem[639] = 2
    x, y = None, None
    pixels = np.zeros((20, 38)).astype(np.object)
    x_candidates = None
    y_candidates = None
    step = 0
    while not computer.done:
        while not computer.done:
            outputs.append(computer.run())
            if outputs[-1] == '_':
                break
        screen = np.array(outputs[:-1]).reshape(-1, 3)
        score_idx = screen[:, 0] == -1
        if score_idx.any():
            score_idx = np.argwhere(score_idx)
            score = screen[score_idx][0, 0, -1]
            screen = np.delete(screen, score_idx, axis=0)
            print(score)
        outputs = []
        screen = screen.astype(np.object)
        screen[screen[:, 2] == 0, 2] = '_'
        screen[screen[:, 2] == 1, 2] = '#'
        screen[screen[:, 2] == 2, 2] = 'X'
        screen[screen[:, 2] == 3, 2] = 'P'
        screen[screen[:, 2] == 4, 2] = 'O'
        pixels[screen[:, 1].astype(np.int), screen[:, 0].astype(np.int)] = screen[:, 2]
        # print(pixels)
        if x is None and y is None:
            xadr, yadr = np.argwhere(pixels == 'O')[0]
            if x_candidates is None:
                x_candidates = set([k for k in computer.program.keys() if computer.program[k] == xadr])
                y_candidates = set([k for k in computer.program.keys() if computer.program[k] == yadr])
            else:
                x_candidates &= set([k for k in computer.program.keys() if computer.program[k] == xadr])
                y_candidates &= set([k for k in computer.program.keys() if computer.program[k] == yadr])
            if len(x_candidates) == 1 and len(y_candidates) == 1:
                x = list(x_candidates)[0]
                y = list(y_candidates)[0]
        else:
            # pass
            # if mem[x] >= 20 - np.argmax(~((pixels != 'X').all(axis=1)[::-1])):
            if step % 200 == 0:
                if not (pixels == 'X').any():
                    break
                block_idx = np.argwhere(pixels == 'X')
                offset = -1  # np.random.choice([-1, 1])
                mem[x] = block_idx[0, 0] + offset
                mem[y] = block_idx[0, 1] + offset

        # if score > 6000:
        # print(pixels, flush=True)
        # time.sleep(0.1)

        step += 1
        if (step % 10000 == 0):
            print(score)
        # print(f"x: {x_candidates}, y: {y_candidates}, done: {computer.done}")
        # joystick = input('input')
        # if joystick == 'd':
        #     computer.inputs.append(-1)
        # elif joystick == 'f':
        #     computer.inputs.append(1)
        # elif joystick == '':
        #     computer.inputs.append(0)
        # else:
        #     break
        computer.inputs.append(0)
    print(score)
