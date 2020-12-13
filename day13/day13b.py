from typing import List, NamedTuple, Tuple


def modplus(a: int, m: int) -> int:
    r = a % m
    if r < 0:
        r += m
    return r


def xgcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return 1, 0, a
    x, y, g = xgcd(b, a % b)
    return y, x - a // b * y, g


def test_xgcd():
    for a in range(-10, 10):
        for b in range(-10, 10):
            x, y, g = xgcd(a, b)
            assert a * x + b * y == g
            if g != 0:
                assert a % g == 0
                assert b % g == 0


class Constraint(NamedTuple):
    # t == b (mod m); t + mx == b
    m: int
    b: int

    def intersection(self, other: 'Constraint') -> 'Constraint':
        x, y, g = xgcd(self.m, other.m)
        m = self.m * other.m // g
        if (other.b - self.b) % g != 0:
            raise Exception('No solution')
        b = self.b - self.m * x * (self.b - other.b) // g
        return Constraint(m=m, b=modplus(b, m))


def solve(consts: List[Constraint]) -> int:
    res = Constraint(m=1, b=0)
    for const in consts:
        res = res.intersection(const)
    return res.b


def parse(text: str) -> List[Constraint]:
    _, line = text.split()
    return [Constraint(m=int(s), b=modplus(-i, int(s))) for i, s in enumerate(line.split(',')) if s != 'x']


def test_solve():
    assert solve(parse("""0
17,x,13,19""")) == 3417
    assert solve(parse("""0
67,7,59,61""")) == 754018
    assert solve(parse("""0
67,x,7,59,61""")) == 779210
    assert solve(parse("""0
67,7,x,59,61""")) == 1261476
    assert solve(parse("""0
1789,37,47,1889""")) == 1202161486
    assert solve(parse("""939
7,13,x,x,59,x,31,19""")) == 1068781


def main():
    with open('day13.txt') as f:
        consts = parse(f.read().strip())
    print(solve(consts))


if __name__ == '__main__':
    main()
