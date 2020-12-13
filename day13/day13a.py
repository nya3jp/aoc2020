from typing import List, Tuple


def solve(start: int, schedule: List[int]) -> int:
    p = min(schedule, key=lambda p: (start + p - 1) // p * p)
    return p * ((start + p - 1) // p * p - start)


def parse(text: str) -> Tuple[int, List[int]]:
    line1, line2 = text.split()
    return int(line1), [int(s) for s in line2.split(',') if s != 'x']


def test_solve():
    assert solve(*parse("""939
7,13,x,x,59,x,31,19""")) == 295


def main():
    with open('day13.txt') as f:
        start, schedule = parse(f.read().strip())
    print(solve(start, schedule))


if __name__ == '__main__':
    main()
