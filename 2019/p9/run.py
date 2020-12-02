from intcode import IntCodeComputer

if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()

    computer = IntCodeComputer(inputs, inputs=[1])
    print(computer.run())
