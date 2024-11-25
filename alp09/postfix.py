import sys
f = sys.argv[1]
postfix = sys.argv[2]

words = []
with open(f) as file:
    word = "0"
    while word != '':
        word = file.readline().strip()
        words.append(word)
words.pop()

shortest = []
number = 0
for word in words:
    isok = True
    for i in range(len(postfix)):
        if postfix[i] != word[i + len(word) - len(postfix)]:
            isok = False
    if isok:
        number += 1
        if len(word) < len(shortest) or len(shortest) == 0:
            shortest = word
print(number)
if number != 0:
    print(shortest)
else:
    print("None")
