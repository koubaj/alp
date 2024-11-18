def myCompare(a, b):
    if a[0] != b[0]:
        return a < b
    order = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
    return order.index(a[1]) < order.index(b[1])

def selectionSort(a):
    for i in range(len(a)):
        mini = i
        for j in range(i+1, len(a)):
            if myCompare(a[j], a[mini]):
            #if a[j] < a[mini]:
                mini = j
        a[i], a[mini] = a[mini], a[i]

def partition(arr, l, r):
    pivot = arr[(l + r) // 2]
    l -= 1
    r += 1
    while True:
        l += 1
        while arr[l] < pivot:
            l += 1
        r -= 1
        while arr[r] > pivot:
            r -= 1
        if l >= r:
            return r
        arr[l], arr[r] = arr[r], arr[l]

def quickSortInternal(arr, l, r):
    if l >= 0 and r >= 0 and l < r:
        pivot = partition(arr, l, r)
        quickSortInternal(arr, pivot + 1, r)
        quickSortInternal(arr, l, pivot)

def quickSort(arr):
    quickSortInternal(arr, 0, len(arr) - 1)

arr = [5, 7, 82 ,1, 5, 3, 4, 17]
cards = [[1, 10], [0, "A"], [3, "J"], [0, 5]]

quickSort(arr)
selectionSort(cards)
print(arr)
