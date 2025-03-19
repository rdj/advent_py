







### Prologue only runs once,
### Initializes d, which is never changed
d = a + 4 * 643
while True:
    a = d

    b = a
    a = 0

    c = 2
    while c > 0:
        if b == 0:
            break
        b -= 1
        c -= 1
    if c == 0:
        a += 1









    if a == 0:
        a = d


