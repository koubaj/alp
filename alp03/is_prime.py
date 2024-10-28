def isPrime(n):
    if n == 1:
        return False
    for i in range(2, int(n**1/2)):
        if n % i == 0:
            return False
    return True

def sexyPrime(n):
    if isPrime(n) and isPrime(n + 6):
        return True
    return False

def div(n):
    ans = []
    for i in range(1, n):
        if n % i == 0:
            ans.append(i)
    return ans

def perfect_num(n):
    if sum(div(n)) == n:
        return True

for i in range(1, 1000):
    if perfect_num(i):
        print(i)
