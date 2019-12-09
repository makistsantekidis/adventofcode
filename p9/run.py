from intcode import IntCodeComputer

if __name__ == '__main__':
    with open('inputs.txt') as f:
        inputs = f.read()

    computer = IntCodeComputer(inputs, setting=2)
    computer.run()
