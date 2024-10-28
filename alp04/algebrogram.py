import copy, sys
eq = []
for l in sys.stdin:
    eq.append(l.strip())

ops = ("+", "-", "*", "/", "=")
var = {} # potential numbers of variables
for j in eq:
    for i in j:
        if i not in ops and i not in var:
            var[i] = list(range(0, 10))

# delete nulls
for i in eq:
    for j in range(0, len(i)):
        if j == 0 or i[j - 1] in ops:
            if var[i[j]][0] == 0:
                var[i[j]].pop(0)

def evaluate(nums, eq):
    equation = ""
    for i in eq:
        if i in ops:
            equation += i
            if i == "=":
                equation += i
        else:
            equation += str(nums[i])
    if not eval(equation):
        return False
    return True


def eq_recursion(eq, var, depth, eq_depth):
    l, r = eq[depth].split("=")

    if eq_depth < len(l):
        if l[eq_depth] in ops:
            eq_depth += 1
        if not isinstance(var[l[eq_depth]], list):
                eq_recursion(eq, var, depth, eq_depth + 1)
                return False

        for i in var[l[eq_depth]]:
            new_var = copy.deepcopy(var)
            new_var[l[eq_depth]] = i
            for key, value in new_var.items():
                if isinstance(value, list) and i in value:
                    new_var[key].remove(i)

            if eq_depth  < len(l):
                eq_recursion(eq, new_var, depth, eq_depth + 1)
        return False

    numbered = ""
    for i in l:
        if i in ops:
            numbered += i
        else:
            numbered += str(var[i])
    computed = eval(numbered)
    
    if computed < 0 or (isinstance(computed, float) and not computed.is_integer()):
        return False

    computed = str(int(computed))
    if len(computed) != len(r):
        return False
    
    for i, j in zip(computed, r):
        if isinstance(var[j], int) and i != str(var[j]):
            return False
        elif isinstance(var[j], list) and int(i) not in var[j]:
            return False
        else:
            var[j] = int(i)
            for key, value in var.items():
                if isinstance(value, list) and int(i) in value:
                    var[key].remove(int(i))

    if not evaluate(var, eq[depth]):
        return False
    
    if depth + 1 < len(eq):
        eq_recursion(eq, copy.deepcopy(var), depth + 1, 0)
    else:
        for i in sorted(var):
            print(var[i], end=" ")
        quit()

eq_recursion(eq, copy.deepcopy(var), 0, 0)

print("NEEXISTUJE")
