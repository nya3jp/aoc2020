from typing import Tuple


def parse_ticket(ticket: str) -> Tuple[int, int]:
    row = int(ticket[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(ticket[7:].replace('L', '0').replace('R', '1'), 2)
    return row, col


def compute_id(row: int, col: int) -> int:
    return row * 8 + col


def test_parse():
    assert parse_ticket('FBFBBFFRLR') == (44, 5)
    assert compute_id(44, 5) == 357
    assert parse_ticket('BFFFBBFRRR') == (70, 7)
    assert compute_id(70, 7) == 567
    assert parse_ticket('FFFBBBFRRR') == (14, 7)
    assert compute_id(14, 7) == 119
    assert parse_ticket('BBFFBBFRLL') == (102, 4)
    assert compute_id(102, 4) == 820


def main():
    tickets = []
    with open('day05.txt') as f:
        for line in f:
            tickets.append(parse_ticket(line.strip()))
    print(max(compute_id(row, col) for row, col in tickets))


if __name__ == '__main__':
    main()
