def PM(arr):
    for i in arr:
        for j in i:
            print(j, end=" ")
        print()

a = [[5, 8, 7, 6], [1, 2, 3, 4]]
print(PM(a))
