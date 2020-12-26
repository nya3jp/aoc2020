import collections
from typing import NamedTuple

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


def solve(input: str) -> int:
    routes = input.strip().splitlines()
    field = collections.defaultdict(bool)
    for route in routes:
        p = coord(route)
        field[p] = not field[p]
    return sum(1 for b in field.values() if b)


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
""")) == 10


def main():
    with open('day24.txt') as f:
        input = f.read()
    print(solve(input))


if __name__ == '__main__':
    main()
