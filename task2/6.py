def evklid_nod(a, b):
    while 1:
        A, B = max(a, b), min(a, b)
        m = A % B
        if m == 0:
            return B

        a, b = B, m


if __name__ == "__main__":
    inp = input()
    a, b = inp.split()
    a, b = int(a), int(b)

    print(evklid_nod(a, b))
