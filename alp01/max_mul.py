nums = list(map(int, input().split()))

now_seq = [0, 0, 0] #p d s
max_seq = now_seq

for j, i in enumerate(nums):
    if i % 3 == 0:
        if now_seq[1] == 0:
            now_seq[0] = j
        now_seq[1] += 1
        now_seq[2] += i
    else:
       now_seq = [0, 0, 0]
    
    if now_seq[1] > max_seq[1]:
       max_seq = now_seq
    elif now_seq[1] == max_seq[1] and now_seq[2] > max_seq[2]:
       max_seq = now_seq
for i in max_seq:
    print(i, end = " ")
