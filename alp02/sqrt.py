x = 0
step = 1
for i in range(10):
    while (x+step)**2 < 625:
        x += step
    step /= 10
print(x)
