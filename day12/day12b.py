from typing import List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, k: int) -> 'Point':
        return Point(k * self.x, k * self.y)

    def rotate(self, degrees: int) -> 'Point':
        assert degrees % 90 == 0, degrees
        times = degrees // 90 % 360
        if times < 0:
            times += 4
        x, y = self.x, self.y
        for _ in range(times):
            x, y = -y, x
        return Point(x, y)


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
    way = Point(10, 1)
    dir = 0
    for inst in insts:
        if inst.op == 'E':
            way = Point(way.x + inst.arg, way.y)
        elif inst.op == 'N':
            way = Point(way.x, way.y + inst.arg)
        elif inst.op == 'W':
            way = Point(way.x - inst.arg, way.y)
        elif inst.op == 'S':
            way = Point(way.x, way.y - inst.arg)
        elif inst.op == 'F':
            pos += way * inst.arg
        elif inst.op == 'L':
            way = way.rotate(inst.arg)
        elif inst.op == 'R':
            way = way.rotate(-inst.arg)
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
F11""")) == 286


def main():
    with open('day12.txt') as f:
        insts = parse(f.read().strip())
    print(solve(insts))


if __name__ == '__main__':
    main()
