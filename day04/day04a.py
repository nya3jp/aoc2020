from typing import Dict, List


Passport = Dict[str, str]


KEYS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')


def solve(passports: List[Passport]) -> int:
    return sum(1 for p in passports if all(k in p for k in KEYS))


def parse(input: str) -> List[Passport]:
    return [
        dict(kv.split(':') for kv in entry.split())
        for entry in input.split('\n\n')]


def test_solve():
    passports = parse("""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""")
    assert solve(passports) == 2


def main():
    with open('day04.txt') as f:
        passports = parse(f.read())
    print(solve(passports))


if __name__ == '__main__':
    main()
