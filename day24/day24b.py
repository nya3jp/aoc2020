import collections
import functools
from typing import NamedTuple, Set


class Point(NamedTuple):
    a: int
    b: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.a + other.a, self.b + other.b)


STEPS = {
    'e': Point(1, 0),
    'w': Point(-1, 0),
    'ne': Point(1, -1),
    'nw': Point(0, -1),
    'se': Point(0, 1),
    'sw': Point(-1, 1),
    'z': Point(0, 0),
}


def coord(route: str) -> Point:
    p = Point(0, 0)
    i = 0
    while i < len(route):
        if route[i] in 'ns':
            step = route[i:i+2]
        else:
            step = route[i:i+1]
        p += STEPS[step]
        i += len(step)
    return p


def simulate(field: Set[Point]) -> Set[Point]:
    candidates = {p + dp for p in field for dp in STEPS.values()}
    new_field = set()
    for p in candidates:
        cnt = sum(1 for dp in STEPS.values() if p + dp in field)
        if p in field and cnt in (2, 3) or p not in field and cnt == 2:
            new_field.add(p)
    return new_field


def solve(input: str) -> int:
    routes = input.strip().splitlines()
    field = {p for p, cnt in collections.Counter(coord(route) for route in routes).items() if cnt % 2 == 1}
    for _ in range(100):
        field = simulate(field)
    return len(field)


def test_solve():
    assert(solve("""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""")) == 2208


def main():
    with open('day24.txt') as f:
        input = f.read()
    print(solve(input))


if __name__ == '__main__':
    main()
