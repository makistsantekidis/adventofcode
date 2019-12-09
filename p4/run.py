import numba
from collections import Counter


# @numba.njit
def count_pass(a, b):
    total = 0
    for i in range(a, b):
        si = [int(s) for s in str(i)]
        dflag = False
        maxi = 0
        for j in range(1, len(si)):
            if si[j] < si[j - 1]:
                dflag = False
                break
            elif si[j] == si[j - 1]:
                dflag = True
                maxi = si[j]
        if dflag:
            # if 2 in list(Counter(si).values()):
            total += 1
    return total


if __name__ == '__main__':
    # print(count_pass(125730, 579381))
    print(count_pass(0, 1000))
    print(count_pass(1000, 2000))
    print(count_pass(2000, 3000))
    print(count_pass(0, 200000))
    print(count_pass(100_000, 200000))
    print(count_pass(200000, 300000))
    print(count_pass(300000, 400000))
    print(count_pass(500000, 600000))
