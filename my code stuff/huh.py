a, b, c = 0
for a in range(0 ,10):
    c = a + 6
    if c >= 10:
        continue
    b = c - 3
    if b < 0:
        continue
    old = 100 * a + 10 * b + c
    new = 1000 * a + 100 * c + b
    print(f"A = {a}, B = {b}, C = {c}, old = {old}, new = {new}, new - old = {new - old}")

    if new > old + 2250:  
        print(f"{old}")