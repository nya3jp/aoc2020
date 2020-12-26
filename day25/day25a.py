MOD = 20201227


def crack(public_key: int) -> int:
    e = 1
    i = 0
    while True:
        if e == public_key:
            return i
        i += 1
        e = e * 7 % MOD


def powmod(a: int, b: int) -> int:
    e = 1
    for _ in range(b):
        e = e * a % MOD
    return e


def main():
    public_keys = (14205034, 18047856)
    print(powmod(public_keys[1], crack(public_keys[0])))


if __name__ == '__main__':
    main()
