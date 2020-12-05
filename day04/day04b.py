import re
from typing import Callable, Dict, List


Passport = Dict[str, str]


def make_year_validator(mini: int, maxi: int) -> Callable[[str], bool]:
    def year_validator(s: str) -> bool:
        if len(s) != 4:
            return False
        try:
            return mini <= int(s) <= maxi
        except ValueError:
            return False
    return year_validator


def validate_height(s: str) -> bool:
    if s.endswith('cm'):
        try:
            return 150 <= int(s[:-2]) <= 193
        except ValueError:
            return False
    if s.endswith('in'):
        try:
            return 59 <= int(s[:-2]) <= 76
        except ValueError:
            return False
    return False


def validate_html_color(s: str) -> bool:
    return bool(re.match(r'^#[0-9a-f]{6}$', s))


def validate_eye_color(s: str) -> bool:
    return s in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def validate_id(s: str) -> bool:
    return bool(re.match(r'^[0-9]{9}$', s))


VALIDATORS = {
    'byr': make_year_validator(1920, 2002),
    'iyr': make_year_validator(2010, 2020),
    'eyr': make_year_validator(2020, 2030),
    'hgt': validate_height,
    'hcl': validate_html_color,
    'ecl': validate_eye_color,
    'pid': validate_id,
}


def validate(p: Passport) -> bool:
    for key, validator in VALIDATORS.items():
        try:
            value = p[key]
        except KeyError:
            return False
        if not validator(value):
            return False
    return True


def solve(passports: List[Passport]) -> int:
    return sum(1 for p in passports if validate(p))


def parse(input: str) -> List[Passport]:
    return [
        dict(kv.split(':') for kv in entry.split())
        for entry in input.split('\n\n')]


def test_solve():
    assert solve(parse("""eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926""")) == 0
    assert solve(parse("""iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946""")) == 0
    assert solve(parse("""hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277""")) == 0
    assert solve(parse("""hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""")) == 0

    assert solve(parse("""pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f""")) == 1
    assert solve(parse("""eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm""")) == 1
    assert solve(parse("""hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022""")) == 1
    assert solve(parse("""iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""")) == 1


def main():
    with open('day04.txt') as f:
        passports = parse(f.read())
    print(solve(passports))


if __name__ == '__main__':
    main()
