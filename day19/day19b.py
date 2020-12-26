import functools
from typing import Dict, List, NamedTuple, Tuple, Union


class CharMatch(NamedTuple):
    char: str


class RefMatch(NamedTuple):
    rule_id: int


class OrMatch(NamedTuple):
    left: 'Match'
    right: 'Match'


class SeqMatch(NamedTuple):
    left: 'Match'
    right: 'Match'


Match = Union[CharMatch, RefMatch, OrMatch, SeqMatch]


def solve_one(rules: Dict[int, Match], text: str) -> int:
    n = len(text)

    @functools.cache
    def solve_rule(i: int, j: int, rule_id: int) -> bool:
        return solve_match(i, j, rules[rule_id])

    def solve_match(i: int, j: int, m: Match) -> bool:
        if isinstance(m, CharMatch):
            return j - i == 1 and text[i] == m.char
        if isinstance(m, RefMatch):
            return solve_rule(i, j, m.rule_id)
        if isinstance(m, OrMatch):
            return solve_match(i, j, m.left) or solve_match(i, j, m.right)
        if isinstance(m, SeqMatch):
            for k in range(i + 1, j):
                if solve_match(i, k, m.left) and solve_match(k, j, m.right):
                    return True
            return False
        assert False, m

    INF = 100
    min31 = [INF] * n + [0]
    for i in reversed(range(n)):
        for j in range(i+1, n+1):
            if solve_rule(i, j, 31):
                min31[i] = min(min31[i], min31[j] + 1)
    max42 = [0] + [-INF] * n
    for j in range(1, n+1):
        for i in range(j):
            if solve_rule(i, j, 42):
                max42[j] = max(max42[j], max42[i] + 1)

    for i in range(1, n):
        if max42[i] > min31[i]:
            return True
    return False


def solve(rules: Dict[int, Match], texts: List[str]) -> int:
    return sum(1 for text in texts if solve_one(rules, text))


def parse_match(expr: str) -> Match:
    if '|' in expr:
        return functools.reduce(OrMatch, (parse_match(subexpr) for subexpr in expr.split(' | ')))
    if ' ' in expr:
        return functools.reduce(SeqMatch, (parse_match(subexpr) for subexpr in expr.split()))
    if '"' in expr:
        return CharMatch(expr.strip('"'))
    return RefMatch(int(expr))


def parse(input: str) -> Tuple[Dict[int, Match], List[str]]:
    rules_section, texts_section = input.strip().split('\n\n')
    rules = {}
    for line in rules_section.splitlines():
        lhs, rhs = line.split(': ')
        rules[int(lhs)] = parse_match(rhs)
    return rules, texts_section.splitlines()


def test_solve():
    assert solve(*parse("""42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""")) == 12


def main():
    with open('day19.txt') as f:
        rules, texts = parse(f.read())
    print(solve(rules, texts))


if __name__ == '__main__':
    main()
