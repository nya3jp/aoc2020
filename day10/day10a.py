import collections
from typing import List


def solve(ns: List[int]) -> int:
    ns = [0] + sorted(ns) + [max(ns) + 3]
    counter = collections.Counter(b - a for a, b in zip(ns, ns[1:]))
    return counter[3] * counter[1]


def test_solve():
    assert solve([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]) == 7 * 5
    assert solve([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]) == 22 * 10


def main():
    with open('day10.txt') as f:
        ns = [int(s) for s in f.read().split()]
    print(solve(ns))


if __name__ == '__main__':
    main()
