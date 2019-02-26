def get_new_p(arr, old_p):
    for i in arr:
        if i is not None and i > old_p:
            return i


def find_primes(n):
    # Решето Эратосфена
    numbers = [i for i in range(2, n)]
    p = 2

    while 1:
        for index, i in enumerate(numbers):
            if i is not None and i >= p ** 2:
                if i % p == 0:
                    numbers[index] = None

        p = get_new_p(numbers, p)
        if p is None or p == n:
            break

    return [i for i in numbers if i is not None]


if __name__ == "__main__":
    n = int(input())
    p = input()
    positions = [int(i)-1 for i in p.split()]

    primes = find_primes(10000)
    strprimes = "".join(str(i) for i in primes)
    print("".join(strprimes[i] for i in positions))
