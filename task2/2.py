#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import os
import random
import re
import sys


# Complete the diagonalDifference function below.

def diagonalDifference(arr):
    n = len(arr)

    s1 = sum([arr[i][i] for i in range(len(arr))])
    s2 = sum([row[-i - 1] for i, row in enumerate(arr)])

    print("s1 = {}, s2 = {}".format(s1, s2))
    return abs(s1 - s2)


if __name__ == '__main__':
    if not 'OUTPUT_PATH' in os.environ:
        os.environ["OUTPUT_PATH"] = "/tmp/output"

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    arr = []

    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    result = diagonalDifference(arr)

    fptr.write(str(result) + '\n')

    fptr.close()
