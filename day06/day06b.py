import functools
from typing import List, Set


def solve(groups: List[List[Set[str]]]) -> int:
    total = 0
    for group in groups:
        intersection = functools.reduce(lambda a, b: a & b, group)
        total += len(intersection)
    return total


def parse(input: str) -> List[List[Set[str]]]:
    groups = []
    for lines in input.strip().split('\n\n'):
        groups.append([set(line) for line in lines.splitlines()])
    return groups


def test_solve():
    assert solve(parse("""abc

a
b
c

ab
ac

a
a
a
a

b
""")) == 6


def main():
    with open('day06.txt') as f:
        input = f.read()
    print(solve(parse(input)))


if __name__ == '__main__':
    main()
