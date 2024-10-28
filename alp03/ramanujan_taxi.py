for c in range(1000, 9999+1):
    bmax=int(c**(1/3)+0.1)
    count = 0
    for b in range(0, bmax):
        a = int((c-b**3)**(1/3)+0.1)
        if a ** 3 + b ** 3 == c and b < a:
            count += 1
            print(a, b, c, count)
    if count == 2:
        quit()
