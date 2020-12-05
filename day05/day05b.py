from typing import Tuple


def parse_ticket(ticket: str) -> Tuple[int, int]:
    row = int(ticket[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(ticket[7:].replace('L', '0').replace('R', '1'), 2)
    return row, col


def compute_id(row: int, col: int) -> int:
    return row * 8 + col


def main():
    tickets = []
    with open('day05.txt') as f:
        for line in f:
            tickets.append(parse_ticket(line.strip()))
    ids = [compute_id(row, col) for row, col in tickets]
    ids.sort()
    for a, b in zip(ids, ids[1:]):
        if b - a == 2:
            print(a+1)


if __name__ == '__main__':
    main()
