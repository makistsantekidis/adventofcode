from operator import add, mul



if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()

    program = [int(i) for i in inputs.split(',')]
    cur_pos = 0

    while program[cur_pos] != 99:
        if program[cur_pos] == 1:
            op = add
        elif program[cur_pos] == 2:
            op = mul
        else:
            raise ValueError("opcode does not exist")
        idx1 = program[cur_pos + 1]
        idx2 = program[cur_pos + 2]
        op_res = op(program[idx1], program[idx2])
        res_idx = program[cur_pos + 3]
        print(f"{op.__name__} to {idx1} and {idx2} into {res_idx}")
        program[res_idx] = op_res
        cur_pos += 4

    print(program)
