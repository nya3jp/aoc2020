import dataclasses
from typing import Optional


N = 1000000


@dataclasses.dataclass
class Node:
    num: int
    decr: Optional['Node'] = None
    next: Optional['Node'] = None


def make_list(seq: str) -> Node:
    nodes = {i: Node(i) for i in range(1, N+1)}
    for i in range(1, N):
        nodes[i+1].decr = nodes[i]
    nodes[1].decr = nodes[N]

    for i in range(N-1):
        a = int(seq[i]) if i < len(seq) else i+1
        b = int(seq[i+1]) if i+1 < len(seq) else i+2
        nodes[a].next = nodes[b]
    nodes[N].next = nodes[int(seq[0])]

    for node in nodes.values():
        assert node.decr, node.num
        assert node.next, node.num

    return nodes[int(seq[0])]


def solve(seq: str, moves: int) -> int:
    current = make_list(seq)
    for _ in range(moves):
        hold = current.next
        current.next = current.next.next.next.next
        target = current.decr
        while target is hold or target is hold.next or target is hold.next.next:
            target = target.decr
        hold.next.next.next = target.next
        target.next = hold
        current = current.next
    while current.num != 1:
        current = current.next
    return current.next.num * current.next.next.num


def disabled_test_solve():
    assert solve('389125467', 10000000) == 149245887792


def main():
    print(solve('123487596', 10000000))


if __name__ == '__main__':
    main()
