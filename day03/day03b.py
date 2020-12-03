from typing import List

STRIDES = (
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1),
)


def solve1(field: List[str], di: int, dj: int) -> int:
    h = len(field)
    w = len(field[0])
    hit = 0
    i, j = 0, 0
    while i < h:
        if field[i][j] == '#':
            hit += 1
        i += di
        j = (j + dj) % w
    return hit


def solve(input: str) -> int:
    field = input.strip().splitlines()
    prod = 1
    for di, dj in STRIDES:
        prod *= solve1(field, di, dj)
    return prod


def test_solve():
    assert solve("""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""") == 336


def main():
    with open('day03.txt') as f:
        input = f.read()
    print(solve(input))


if __name__ == '__main__':
    main()
