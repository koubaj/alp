i = 1
val = 1/(i*(1.1)**i)
print(val)
while val >= 0.01:
    print(val)
    i += 1
    val = 1/(i*(1.1)**i)
