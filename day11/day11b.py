from typing import List


def extend_seats(seats: List[str]) -> List[str]:
    w = len(seats[0])
    return ['.' * (w+2)] + ['.' + row + '.' for row in seats] + ['.' * (w+2)]


def next_tick(seats: List[str]) -> List[str]:
    h = len(seats)
    w = len(seats[0])

    def next_cell(i: int, j: int) -> str:
        if seats[i][j] == '.':
            return '.'
        c = 0
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                k = 1
                while True:
                    ii = i + di * k
                    jj = j + dj * k
                    if ii < 0 or ii >= h or jj < 0 or jj >= w:
                        break
                    if seats[ii][jj] == '#':
                        c += 1
                    if seats[ii][jj] != '.':
                        break
                    k += 1
        if seats[i][j] == 'L' and c == 0:
            return '#'
        if seats[i][j] == '#' and c >= 5:
            return 'L'
        return seats[i][j]

    return [''.join(next_cell(i, j) for j in range(w)) for i in range(h)]


def solve(seats: List[str]) -> int:
    seats = extend_seats(seats)
    while True:
        new_seats = next_tick(seats)
        if new_seats == seats:
            return ''.join(seats).count('#')
        seats = new_seats


def test_solve():
    assert solve("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()) == 26


def main():
    with open('day11.txt') as f:
        seats = f.read().rstrip().splitlines()
    print(solve(seats))


if __name__ == '__main__':
    main()
