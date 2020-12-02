import numpy as np

if __name__ == '__main__':
    inputs = np.array(list(open('inputs.txt').read()), dtype=np.int)
    layers = inputs.reshape(25, 6, -1, order='F').transpose((1, 0, 2))
    idxs = np.argmax(layers != 2, axis=2).flatten()
    print(layers.reshape(6 * 25, -1)[np.arange(150), idxs.flatten()].reshape(6, 25))
