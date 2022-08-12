import numpy as np


def normal():
    x = np.arange(15, dtype=np.int64).reshape(3, 5)
    x[1:, ::2] = -99
    print(x)
    # array([[  0,   1,   2,   3,   4],
    #        [-99,   6, -99,   8, -99],
    #        [-99,  11, -99,  13, -99]])

    x.max(axis=1)
    # array([ 4,  8, 13])

    # Generate normally distributed random numbers:
    rng = np.random.default_rng()
    samples = rng.normal(size=2500)
    print(samples)


if __name__ == "__main__":
    normal()
    pass
