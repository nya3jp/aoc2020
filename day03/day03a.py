def solve(input: str) -> int:
    field = input.strip().splitlines()
    w = len(field[0])
    hit = 0
    for i, row in enumerate(field):
        j = (i * 3) % w
        if row[j] == '#':
            hit += 1
    return hit


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
""") == 7


def main():
    with open('day03.txt') as f:
        input = f.read()
    print(solve(input))


if __name__ == '__main__':
    main()
