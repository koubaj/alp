n, m, s = map(int, input().split())
temp = list(map(int, input().split()))
nums = [[0] * m for i in range(n)]
for i in range(n):
    for j in range(m):
        nums[i][j] = temp[i * m + j]

temp = input()
lets = [[0] * m for i in range(n)]
for i in range(n):
    for j in range(m):
        lets[i][j] = temp[i * m + j]

moves = ((1, 0), (0, 1), (-1, 0), (0, -1))
out = ""
for i in range(int(m / s)):
    for j in range(int(n / s)):
        maxi = -9999999999999
        pos = [n, m]
        for k in range(s):
            for l in range(s):
                noffset = j * s
                moffset = i * s
                np = noffset + k
                mp = moffset + l

                val = nums[np][mp]
                for a in moves:
                    anp = (np + a[0] - noffset) % s + noffset
                    amp = (mp + a[1] - moffset) % s + moffset
                    val += nums[anp][amp]
                if val > maxi:
                    maxi = val
                    pos = [np, mp]
        out += lets[pos[0]][pos[1]]
print(out)
