from typing import List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, k: int) -> 'Point':
        return Point(k * self.x, k * self.y)


DIRS = (
    Point(+1, 0),
    Point(0, +1),
    Point(-1, 0),
    Point(0, -1),
)


class Instruction(NamedTuple):
    op: str
    arg: int


def solve(insts: List[Instruction]) -> int:
    pos = Point(0, 0)
    dir = 0
    for inst in insts:
        if inst.op == 'E':
            pos = Point(pos.x + inst.arg, pos.y)
        elif inst.op == 'N':
            pos = Point(pos.x, pos.y + inst.arg)
        elif inst.op == 'W':
            pos = Point(pos.x - inst.arg, pos.y)
        elif inst.op == 'S':
            pos = Point(pos.x, pos.y - inst.arg)
        elif inst.op == 'F':
            pos += DIRS[dir] * inst.arg
        elif inst.op == 'L':
            dir = (dir + inst.arg // 90) % 4
        elif inst.op == 'R':
            dir = (dir + (360 - inst.arg) // 90) % 4
        else:
            raise Exception('Unknown operation: %s %d' % (inst.op, inst.arg))
    return abs(pos.x) + abs(pos.y)


def parse(text: str) -> List[Instruction]:
    insts = []
    for line in text.splitlines():
        insts.append(Instruction(
            op=line[0],
            arg=int(line[1:])))
    return insts


def test_solve():
    assert solve(parse("""F10
N3
F7
R90
F11""")) == 25


def main():
    with open('day12.txt') as f:
        insts = parse(f.read().strip())
    print(solve(insts))


if __name__ == '__main__':
    main()
