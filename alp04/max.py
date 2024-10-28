small_int = -999999999999

def myMax(arr):
    max_til = small_int 
    for i in arr:
        if i > max_til:
            max_til = i
    return max_til

def secondMax(arr):
    arr = arr.copy()
    highest = myMax(arr)
    for i in range(len(arr)):
        if arr[i] == highest:
            arr[i] = small_int 
    return myMax(arr)

def secondMax2(arr):
    first = small_int
    second = first
    for i in arr:
        if i > first:
            second = first
            first = i
        elif i > second:
            second = i
    return second


arr = [5, 8, 7, -15, 871, 15]
print(secondMax2(arr))
