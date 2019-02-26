def evklid_nod(a, b):
    while 1:
        _a, _b = max(a, b), min(a, b)
        m = _a % _b
        if m == 0:
            return _b

        a, b = _b, m


if __name__ == "__main__":
    inp = input()
    a, b = inp.split()
    a, b = int(a), int(b)

    print(evklid_nod(a, b))
