nums = list(map(int, input().split()))
nums.sort()
num = int(input())
cache = []

def recursion(ans, not_used, nums, num):
    if ans != "" and ans[0] == " ":
        ans = ans[3:]
        
    val = 0 if ans == "" else eval(ans)
    if val == num:
        print(ans)
        quit()
    if val > num or ans in cache:
        return False
    
    for c, i in enumerate(not_used):
        recursion(ans + f" + {i}", not_used[:c]+not_used[c+1:], nums, num)
        recursion(ans + f" * {i}", not_used[:c]+not_used[c+1:], nums, num)
    cache.append(ans)

recursion("", nums, nums, num)
print("NEEXISTUJE")
