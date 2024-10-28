import math

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million", "billion", "trillion", "quadrillion"]


def find_error(numbers, num):
    if num.isnumeric():
        return False
    
    num = list(map(str, num.split()))

    for i in num:
        if i not in numbers:
            return True
    
    if num.index(num[0]) >= 27:
        return True
    for i in range(1, len(num)):
        ni = numbers.index(num[i])
        bi = numbers.index(num[i-1])
        if ni < 9 and bi < 19:
            return True
        elif ni >= 9 and ni < 19 and bi < 27:
            return True
        elif ni >= 19 and ni < 27 and bi < 27:
            return True
        elif ni == 27 and bi >= 9:
            return True
        elif ni >= 27 and ni < 33 and bi >= 28:
            return True
    
    last_big = 9999
    for i in num:
        ni = numbers.index(i) 
        if ni > 27:
            if ni >= last_big:
                return True
            else:
                last_big = ni

    return False      


def addout(out, index):
    return out + numbers[index] + " "

def to_text(numbres, num):
    out = ""
    
    n = []
    for i in range(len(num) - 3, -1, -3):
        n.append(num[i:min(i+3, len(num))])
    if len(num)%3 != 0:
        n.append(num[0:len(num)%3])
    n = n[::-1]

    for count, i in enumerate(n):
        i = i[::-1]
        added = False
        
        if len(i) == 3 and i[2] != '0':
            out = addout(out, int(i[2]) - 1)
            out = addout(out, 27)
            added = True
        if len(i) >= 2 and int(i[1]) < 2:
            if int(i[1] + i[0]) != 0:
                out = addout(out, int(i[1] + i[0]) - 1)
                added = True
        else:
            if len(i) >= 2:
                out = addout(out, int(i[1]) + 17)
                added = True
            if i[0] != "0":
                out = addout(out, int(i[0]) - 1)
                added = True

        if added and count < len(n) - 1:
            out = addout(out, 32 - (6 - math.ceil(len(num) / 3)) - count)

    return out

def to_int(numbers, num):
    out = 0
    if 'hundred' in num:
        out += 100 * (numbers.index(num[0]) + 1)
        num = num[2:]
    for i in num:
        ni = numbers.index(i)
        if ni < 19:
            out += ni + 1
        elif ni < 27:
            out += 10 * (ni - 17)
        elif ni > 27:
            out *= 10**(3*(ni-27))

    return out

def to_num(numbers, num):
    out = 0
    num = list(map(str, num.split()))

    temp = []
    for i in num:
        temp.append(i)
        if numbers.index(i) > 27:
            out += to_int(numbers, temp)
            temp = []
    out += to_int(numbers, temp)

    return out


num = str(input())
if find_error(numbers, num):
    print("ERROR")
    quit()
if num.isnumeric():
    print(to_text(numbers, num))
else:
    print(to_num(numbers, num))
