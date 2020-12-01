from typing import List, Optional


def solve(ns: List[int]) -> Optional[int]:
    for i, a in enumerate(ns):
        bs = ns[i+1:]
        for j, b in enumerate(bs):
            cs = bs[j+1:]
            for c in cs:
                if a + b + c == 2020:
                    return a * b * c
    return None


def test_solve():
    assert solve([1721, 979, 366, 299, 675, 1456]) == 241861950


def main():
    with open('day01.txt') as f:
        ns = [int(s) for s in f.read().split()]
    print(solve(ns))


if __name__ == '__main__':
    main()
