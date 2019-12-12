from copy import copy
from operator import add, mul, lt, eq
from collections import defaultdict, deque

op_dict = {
    1: add, 2: mul, 7: lt, 8: eq
}
instr_steps = {
    1: 4, 2: 4, 3: 2, 4: 2, 5: 0, 6: 0,
    7: 4, 8: 4, 9: 2,
}


class IntCodeComputer:
    def __init__(self, program, inputs=[], interactive=False):
        self.program_str = copy(program)
        self.pos = 0
        self.relative_base = 0
        self.program = defaultdict(lambda: 0)
        for i, p in enumerate(([int(i) for i in self.program_str.split(',')])):
            self.program[i] = p
        self.inputs = deque(inputs)
        self.interactive = interactive
        self.done = False

    def get_value(self, param, opcode):
        if opcode == 1:
            return param
        elif opcode == 2:
            return self.program[param + self.relative_base]
        elif opcode == 0:
            return self.program[param]

    def get_address(self, param, opcode):
        if opcode == 2:
            return param + self.relative_base
        else:
            return param

    def run(self):
        program = self.program
        last_out = None
        while program[self.pos] != 99:
            operation = program[self.pos]
            ops = [int(i) for i in f"{operation:05}"]
            opcode = ops[-1] + 10 * ops[-2]
            if opcode in [1, 2]:
                op = op_dict[opcode]
                v1 = self.get_value(program[self.pos + 1], ops[-3])
                v2 = self.get_value(program[self.pos + 2], ops[-4])
                op_res = op(v1, v2)
                resv = self.get_address(program[self.pos + 3], ops[-5])
                # print(f"{op.__name__} to {v1} and {v2} into {resv}")
                program[resv] = op_res
            elif opcode == 3:
                # inp = input('Give input:')
                adr = self.get_address(program[self.pos + 1], ops[-3])
                if len(self.inputs) > 0:
                    program[adr] = self.inputs.popleft()
                else:
                    return '_'
            elif opcode == 4:
                val = self.get_value(program[self.pos + 1], ops[-3])
                # print(program[self.pos], program[self.pos + 1])
                # print(val)
                last_out = val
                if self.interactive:
                    self.pos += instr_steps[opcode]
                    return val
            elif opcode in [5, 6]:
                v1 = self.get_value(program[self.pos + 1], ops[-3])
                v2 = self.get_value(program[self.pos + 2], ops[-4])
                do_move = (v1 != 0 and opcode == 5) or (v1 == 0 and opcode == 6)
                if do_move:
                    # print(f"Jumping to {self.pos}")
                    self.pos = v2
                else:
                    self.pos += 3
            elif opcode in [7, 8]:
                op = op_dict[opcode]
                v1 = self.get_value(program[self.pos + 1], ops[-3])
                v2 = self.get_value(program[self.pos + 2], ops[-4])
                resv = self.get_address(program[self.pos + 3], ops[-5])
                # print(f"{op.__name__} to {v1} and {v2} into {resv}")
                program[resv] = 1 if op(v1, v2) else 0
            elif opcode == 9:
                v1 = self.get_value(program[self.pos + 1], ops[-3])
                self.relative_base += v1
            self.pos += instr_steps[opcode]
        self.done = True
        self.pos += 1
        operation = program[self.pos]
        ops = [int(i) for i in f"{operation:05}"]
        opcode = ops[-1] + 10 * ops[-2]
        if opcode == 4:
            val = self.get_value(program[self.pos + 1], ops[-3])
            # print(program[self.pos], program[self.pos + 1])
            print(val)
        return 'done'
