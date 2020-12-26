def decr(c: str) -> str:
    if c == '1':
        return '9'
    return chr(ord(c) - 1)


def solve(seq: str, moves: int) -> str:
    for _ in range(moves):
        hold = seq[1:4]
        seq = seq[0] + seq[4:]
        target = decr(seq[0])
        while True:
            try:
                pos = seq.index(target)
                break
            except ValueError:
                target = decr(target)
        seq = seq[:pos+1] + hold + seq[pos+1:]
        seq = seq[1:] + seq[0]
    pos = seq.index('1')
    return seq[pos+1:] + seq[:pos]


def test_solve():
    assert solve('389125467', 10) == '92658374'
    assert solve('389125467', 100) == '67384529'


def main():
    print(solve('123487596', 100))


if __name__ == '__main__':
    main()
