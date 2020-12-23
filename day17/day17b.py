from typing import NamedTuple, Set


class P(NamedTuple):
    x: int
    y: int
    z: int
    w: int

    def __add__(self, other: 'P') -> 'P':
        return P(self.x+other.x, self.y+other.y, self.z+other.z, self.w+other.w)


NEIGHBORS = [
    P(x, y, z, w)
    for x in (-1, 0, 1)
    for y in (-1, 0, 1)
    for z in (-1, 0, 1)
    for w in (-1, 0, 1)
    if x != 0 or y != 0 or z != 0 or w != 0
]


State = Set[P]


def parse(input: str) -> State:
    state = set()
    for y, row in enumerate(input.strip().splitlines()):
        for x, cell in enumerate(row):
            if cell == '#':
                state.add(P(x, y, 0, 0))
    return state


def simulate(state: State) -> State:
    next_state = set()
    for p in state | set(p + dp for p in state for dp in NEIGHBORS):
        cnt = 0
        for dp in NEIGHBORS:
            if p + dp in state:
                cnt += 1
        if (p in state and cnt in (2, 3)) or (p not in state and cnt == 3):
            next_state.add(p)
    return next_state


def solve(state: State) -> int:
    for _ in range(6):
        state = simulate(state)
    return len(state)


def slow_test_solve():
    assert solve(parse(""".#.
..#
###
""")) == 848


def main():
    with open('day17.txt') as f:
        state = parse(f.read())
    print(solve(state))


if __name__ == '__main__':
    main()
