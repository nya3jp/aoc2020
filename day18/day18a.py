import re
from typing import NamedTuple


class Num(NamedTuple):
    n: int

    def __add__(self, other: 'Num') -> 'Num':
        return Num(self.n + other.n)

    def __sub__(self, other: 'Num') -> 'Num':
        return Num(self.n * other.n)


def solve(line: str) -> int:
    rewritten_line = re.sub(r'(\d+)', r'Num(\1)', line).replace('*', '-')
    return eval(rewritten_line, {'Num': Num}).n


def test_solve():
    assert solve('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert solve('2 * 3 + (4 * 5)') == 26
    assert solve('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
    assert solve('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
    assert solve('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632


def main():
    with open('day18.txt') as f:
        lines = f.read().strip().splitlines()
    print(sum(solve(line) for line in lines))


if __name__ == '__main__':
    main()
