from typing import List


def has_pair(ns: List[int], sum: int) -> bool:
    for i, a in enumerate(ns):
        for b in ns[i+1:]:
            if a + b == sum:
                return True
    return False


def solve(seq: List[int], size: int) -> int:
    for i in range(size, len(seq)):
        if not has_pair(seq[i-size:i], seq[i]):
            return seq[i]
    raise Exception('Solution not found')


def test_solve():
    seq = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
    assert solve(seq, 5) == 127


def main():
    with open('day09.txt') as f:
        seq = [int(s) for s in f.read().split()]
    print(solve(seq, 25))


if __name__ == '__main__':
    main()
