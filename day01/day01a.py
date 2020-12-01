from typing import List, Optional


def solve(ns: List[int]) -> Optional[int]:
    for i, a in enumerate(ns):
        for b in ns[i+1:]:
            if a + b == 2020:
                return a * b
    return None


def test_solve():
    assert solve([1721, 979, 366, 299, 675, 1456]) == 514579


def main():
    with open('day01.txt') as f:
        ns = [int(s) for s in f.read().split()]
    print(solve(ns))


if __name__ == '__main__':
    main()
