from intcode import IntCodeComputer
from itertools import permutations
from tqdm import tqdm


def run(program, phase, power):
    computer = IntCodeComputer(program, inputs=[phase, power])
    return computer.run()


def run_to_completion(program, phase_config):
    computers = [IntCodeComputer(program, inputs=[p], interactive=True) for p in phase_config]
    pow = 0
    while True:
        for c in computers:
            c.inputs.append(pow)
            pow_ = c.run()
            if c.done:
                break
            pow = pow_
        if c.done:
            break
    return pow


if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()

    # ps = list(range(5))
    # maxpow = 0
    # for conf in permutations(ps):
    #     pow = 0
    #     for s in conf:
    #         pow = run(inputs, s, pow)
    #     maxpow = max(pow, maxpow)
    # print(maxpow)
    ps = list(range(5, 10))
    maxpow = 0
    for conf in tqdm(permutations(ps)):
        pow = run_to_completion(inputs, conf)
        maxpow = max(pow, maxpow)
    print(maxpow)
