import functools
from typing import Dict, List, NamedTuple, Optional, Set


class Food(NamedTuple):
    ingredients: Set[str]
    allergens: Set[str]


def bipartite_match(graph: Dict[str, List[str]], exclude_right: str) -> int:
    matching = {}

    def augment(left: Optional[str], visited: Set[str]) -> bool:
        if left is None:
            return True
        if left in visited:
            return False
        visited.add(left)
        for right in graph[left]:
            if right == exclude_right:
                continue
            if augment(matching.get(right), visited):
                matching[right] = left
                return True
        return False

    for left in graph:
        augment(left, set())

    return len(matching)


def solve(foods: List[Food]) -> int:
    all_allergens = functools.reduce(lambda a, b: a | b, (food.allergens for food in foods))
    all_ingredients = functools.reduce(lambda a, b: a | b, (food.ingredients for food in foods))
    graph = {
        allergen: functools.reduce(lambda a, b: a & b, (food.ingredients for food in foods if allergen in food.allergens))
        for allergen in all_allergens
    }

    safe_ingredients = []
    for ingredient in all_ingredients:
        if bipartite_match(graph, ingredient) == len(all_allergens):
            safe_ingredients.append(ingredient)

    return sum(1 for ingredient in safe_ingredients for food in foods if ingredient in food.ingredients)


def parse(input: str) -> List[Food]:
    foods = []
    for line in input.strip().splitlines():
        lhs, rhs = line.rstrip(')').split(' (contains ')
        foods.append(Food(ingredients=set(lhs.split()), allergens=set(rhs.split(', '))))
    return foods


def test_solve():
    assert solve(parse("""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""")) == 5


def main():
    with open('day21.txt') as f:
        foods = parse(f.read())
    print(solve(foods))


if __name__ == '__main__':
    main()
