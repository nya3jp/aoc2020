from typing import List, Tuple


def score(deck: List[int]):
    n = len(deck)
    return sum(card * (n - i) for i, card in enumerate(deck))


def solve(deck0: List[int], deck1: List[int]) -> Tuple[bool, int]:
    memo = set()
    while deck0 and deck1:
        state = (tuple(deck0), tuple(deck1))
        if state in memo:
            return True, -1
        memo.add(state)
        card0 = deck0.pop(0)
        card1 = deck1.pop(0)
        if len(deck0) >= card0 and len(deck1) >= card1:
            win = solve(deck0[:card0], deck1[:card1])[0]
        else:
            win = card0 > card1
        if win:
            deck0.extend([card0, card1])
        else:
            deck1.extend([card1, card0])
    return bool(deck0), score(deck0 or deck1)


def parse(input: str) -> Tuple[List[int], List[int]]:
    section0, section1 = input.strip().split('\n\n')
    return [int(s) for s in section0.splitlines()[1:]], [int(s) for s in section1.splitlines()[1:]]


def test_solve():
    assert solve(*parse("""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""")) == (False, 291)


def main():
    with open('day22.txt') as f:
        decks = parse(f.read())
    print(solve(*decks))


if __name__ == '__main__':
    main()
