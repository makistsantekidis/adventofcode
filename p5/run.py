from operator import add, mul, lt, eq
from intcode import IntCodeComputer

op_dict = {
    1: add, 2: mul, 7: lt, 8: eq
}
instr_steps = {
    1: 4, 2: 4, 3: 2, 4: 2, 5: 0, 6: 0,
    7: 4, 8: 4,
}

if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()
    pos = 0
    program = [int(i) for i in inputs.split(',')]

    while program[pos] != 99:
        operation = program[pos]
        ops = [int(i) for i in f"{operation:05}"]
        opcode = ops[-1] + 10 * ops[-2]
        if opcode in [1, 2]:
            op = op_dict[opcode]
            v1 = program[pos + 1]
            v2 = program[pos + 2]
            v1 = v1 if ops[-3] == 1 else program[v1]
            v2 = v2 if ops[-4] == 1 else program[v2]
            op_res = op(v1, v2)
            resv = program[pos + 3]
            # print(f"{op.__name__} to {v1} and {v2} into {resv}")
            program[resv] = op_res
        elif opcode == 3:
            # inp = input('Give input:')
            # print('Giving input 5')
            adr = program[pos + 1]
            program[adr] = 5
        elif opcode == 4:
            adr = program[pos + 1]
            val = adr if ops[-3] == 1 else program[adr]
            print(val)
        elif opcode in [5, 6]:
            v1 = program[pos + 1]
            v2 = program[pos + 2]
            v1 = v1 if ops[-3] == 1 else program[v1]
            v2 = v2 if ops[-4] == 1 else program[v2]
            do_move = (v1 != 0 and opcode == 5) or (v1 == 0 and opcode == 6)
            if do_move:
                # print(f"Jumping to {pos}")
                pos = v2
            else:
                pos += 3
        elif opcode in [7, 8]:
            op = op_dict[opcode]
            v1 = program[pos + 1]
            v2 = program[pos + 2]
            v1 = v1 if ops[-3] == 1 else program[v1]
            v2 = v2 if ops[-4] == 1 else program[v2]
            resv = program[pos + 3]
            # print(f"{op.__name__} to {v1} and {v2} into {resv}")
            program[resv] = 1 if op(v1, v2) else 0
        pos += instr_steps[opcode]

    pos += 1
    if len(program) > pos:
        if program[pos] == 4:
            print(program[pos + 1])

    print("_________")

    computer = IntCodeComputer(inputs, setting=5)
    computer.run()
