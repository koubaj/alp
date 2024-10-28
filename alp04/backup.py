def recursion(eq, var, blacklist):
    pos = ""
    done_vars = []
    for key, value in var.items():
        done_vars.append(key)
        if isinstance(value, list):
            pos = key
            break
   
    if pos == "":
        if evaluate(var, eq):
            for i in sorted(var):
                print(var[i], end=" ")
            quit()
        else:
            return False


    for i in range(len(var[pos])):
        if var[pos][i] not in blacklist:
            new_var = var.copy()
            new_var[pos] = var[pos][i]
            new_blacklist = blacklist.copy()
            new_blacklist.append(var[pos][i])
            
            continuei = False
            test_eq = []
            for j in eq:
                not_complete = False
                eq_pos = 0
                eq_left = ""

                while j[eq_pos] != "=":
                    if j[eq_pos] not in ops and j[eq_pos] not in done_vars:
                        not_complete = True
                        break
                    if j[eq_pos] in ops:
                        eq_left += str(j[eq_pos])
                    else:
                        eq_left += str(new_var[j[eq_pos]])
                    eq_pos += 1
                if not_complete:
                    continue
               
                res = "".join([j[k] for k in range(eq_pos + 1, len(j))])
                eq_res = eval(eq_left)

                if eq_res < 0 or not isinstance(eq_res, int):
                    continuei = True
                    break
                eq_res = str(eq_res)
                if len(eq_res) != len(res):
                    continuei = True
                    break

                quitj = False
                for count, k in enumerate(res):
                    if isinstance(new_var[k], list):
                        new_var[k] = eq_res[count]
                    elif new_var[k] != eq_res[count]:
                        quitj = True
                        break
                if quitj:
                    continuei = True
                    break
                test_eq.append(j)

            if continuei:
                continue

            test_var = {}
            for key, value in new_var.items():
                test_var[key] = value

            if evaluate(test_var, test_eq):
                recursion(eq, new_var, new_blacklist)

