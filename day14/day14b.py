import re
from typing import List


SET_RE = re.compile(r'^mem\[(\d+)\] = (\d+)$')


def solve(program: str) -> int:
    mask = '0' * 36
    mem = {}
    for line in program.strip().splitlines():
        if line.startswith('mask = '):
            mask = line.split()[2]
            continue
        m = SET_RE.match(line)
        assert m, line
        base_addr = int(m.group(1))
        value = int(m.group(2))

        def write(i: int, addr: int):
            if i == 36:
                mem[addr] = value
            elif mask[i] == '0':
                write(i+1, addr)
            elif mask[i] == '1':
                write(i+1, addr | 1 << (35-i))
            elif mask[i] == 'X':
                write(i+1, addr)
                write(i+1, addr ^ 1 << (35-i))
            else:
                assert False

        write(0, base_addr)
    return sum(mem.values())


def test_solve():
    assert solve("""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""") == 208


def main():
    with open('day14.txt') as f:
        program = f.read()
    print(solve(program))


if __name__ == '__main__':
    main()
