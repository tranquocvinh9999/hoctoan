# nhân cộng trừ
import math
import random

def nhan():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    res = a * b
    return a, b, res

def cong():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    res = a + b
    return a, b, res

def tru():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    if a >= b:
        res = a - b
    else:
        res = b - a
    return a, b, res
