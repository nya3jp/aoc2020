from typing import List


def solve(seq: List[int], n: int) -> int:
    recent = {}
    for i, a in enumerate(seq[:-1]):
        recent[a] = i
    last = seq[-1]
    for i in range(len(seq), n):
        if last in recent:
            next = i - recent[last] - 1
        else:
            next = 0
        recent[last] = i - 1
        last = next
    return last


def parse(text: str) -> List[int]:
    return [int(s) for s in text.split(',')]


def test_solve():
    assert solve(parse('0,3,6'), 2020) == 436
    assert solve(parse('1,3,2'), 2020) == 1
    assert solve(parse('2,1,3'), 2020) == 10
    assert solve(parse('1,2,3'), 2020) == 27
    assert solve(parse('2,3,1'), 2020) == 78
    assert solve(parse('3,2,1'), 2020) == 438
    assert solve(parse('3,1,2'), 2020) == 1836


def disabled_test_solve_heavy():
    assert solve(parse('0,3,6'), 30000000) == 175594
    assert solve(parse('1,3,2'), 30000000) == 2578
    assert solve(parse('2,1,3'), 30000000) == 3544142
    assert solve(parse('1,2,3'), 30000000) == 261214
    assert solve(parse('2,3,1'), 30000000) == 6895259
    assert solve(parse('3,2,1'), 30000000) == 18
    assert solve(parse('3,1,2'), 30000000) == 362


def main():
    print(solve(parse('0,13,16,17,1,10,6'), 30000000))


if __name__ == '__main__':
    main()
