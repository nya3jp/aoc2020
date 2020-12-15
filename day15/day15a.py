from typing import List


def solve(seq: List[int], n: int) -> int:
    while len(seq) < n:
        for i in range(2, len(seq)+1):
            if seq[-i] == seq[-1]:
                seq.append(i-1)
                break
        else:
            seq.append(0)
    return seq[n-1]


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


def main():
    print(solve(parse('0,13,16,17,1,10,6'), 2020))


if __name__ == '__main__':
    main()
