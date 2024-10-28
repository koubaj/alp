base = int(input())
nums  = [input() for i in range(3)]


chars = ['0'] * 36
for i in range(10):
    chars[i] = chr(i + 48)
for i in range(26):
    chars[i+10] = chr(ord('a') + i)

error = False
for i in nums:
    dots = 0
    for j in i:
        if j == '.':
            dots += 1
        if j != '.' and chars.index(j) > base - 1:
            error = True
    if dots != 1:
        error = True

def add_char(a, b):
    return chars.index(a) + chars.index(b)
def sub_char(a, b):
    return chars.index(a) - chars.index(b)

def operation(a, b, op): #t=+; f=-
    dec_a = len(a) - a.index('.') - 1
    dec_b = len(b) - b.index('.') - 1   
    nat_a = len(a) - dec_a - 1
    nat_b = len(b) - dec_b - 1

    for i in range(abs(dec_a - dec_b)):
        if dec_a < dec_b:
            a += '0'
        else:
            b += '0'

    for i in range(abs(nat_a - nat_b)):
        if nat_a < nat_b:
            a = '0' + a
        else:
            b = '0' + b
    a = '0' + a
    b = '0' + b

    out = ""
    before = 0

    minus = False
    if not op:
        for i in range(len(a)):
            if a[i] < b[i]:
                minus = True
                a, b = b, a
                break
            elif a[i] > b[i]:
                break

    for i in range(len(a) - 1, -1, -1):
        if a[i] == '.':
            out += '.'
            continue
        if op:
            out += chars[(add_char(a[i], b[i]) + before) % base]
            before = (add_char(a[i], b[i]) + before) // base
        else:
            out += chars[(sub_char(a[i], b[i]) + before) % base]
            before = (sub_char(a[i], b[i]) + before) // base
    
    out = out[::-1]

    for i in out:
        if i != '0':
            break
        out = out[1:]

    if minus:
        out = '-' + out

    return(out)
            

if error:
    print("ERROR")
else:
    after_add = operation(nums[0], nums[1], True)
    after_sub = operation(after_add, nums[2], False)

    print(after_sub)
