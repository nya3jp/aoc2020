import re
from typing import Dict, List, NamedTuple, Tuple


ForwardGraph = Dict[str, List[Tuple[int, str]]]
BackwardGraph = Dict[str, List[str]]


RULE_RE = re.compile(
    r'^(?P<outer>\S+ \S+ bags) contain '
    r'(?:no other bags|(?P<inners>(?:\d+ \S+ \S+ bags?(?:, )?)+))\.$')


def parse_bag(s: str) -> (int, str):
    v = s.split()
    assert len(v) == 4
    return int(v[0]), ' '.join(v[1:3])


def parse(input: str) -> ForwardGraph:
    graph = {}
    for line in input.strip().splitlines():
        m = RULE_RE.match(line)
        assert m, line
        outer = parse_bag('0 ' + m.group('outer'))[1]
        inners_str = m.group('inners')
        inners = [parse_bag(s) for s in inners_str.split(', ')] if inners_str else []
        graph[outer] = inners
    return graph


def make_reverse(graph: ForwardGraph) -> BackwardGraph:
    revgraph = {}
    for outer, inners in graph.items():
        for _, inner in inners:
            revgraph.setdefault(inner, []).append(outer)
    return revgraph


def solve(graph: ForwardGraph) -> int:
    revgraph = make_reverse(graph)
    seen = set()

    def search(inner: str) -> None:
        if inner in seen:
            return
        seen.add(inner)
        for outer in revgraph.get(inner, []):
            search(outer)

    search('shiny gold')
    return len(seen) - 1


def test_parse():
    assert parse("""light red bags contain 1 bright white bag, 2 muted yellow bags.
bright white bags contain 1 shiny gold bag.
faded blue bags contain no other bags.
""") == {
        'light red': [(1, 'bright white'), (2, 'muted yellow')],
        'bright white': [(1, 'shiny gold')],
        'faded blue': [],
    }


def test_solve():
    assert solve(parse("""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""")) == 4


def main():
    with open('day07.txt') as f:
        input = f.read()
    print(solve(parse(input)))


if __name__ == '__main__':
    main()
