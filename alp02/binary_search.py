l = 0
r = 1000
k = float(input())

if k < 0:
    print("invalid")
    quit()

def f(x):
    return x ** 2 - k

while abs(l-r) > 0.01:
    m = (l + r) / 2
    fl = f(l)
    fm = f(m)
    fr = f(r)

    if (fm > 0 and fr > 0) or (fm < 0 and fr < 0):
        r = m
    if (fl > 0 and fm > 0) or (fl < 0 and fm < 0):
        l = m
    print(l, r, f(m))
