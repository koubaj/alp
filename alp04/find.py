def find(text, word):
    if len(word) == 0:
        return -1
    for i in range(len(text)):
        if text[i] == word[0]:
            found = True
            for j in range(len(word)):
                if i + j >= len(text):
                    found = False
                elif word[j] != text[i + j]:
                    found = False
                    break
            if found:
                return i
    return -1

def replace(text, word, new):
    pos = find(text, word)
    if pos == -1:
        return text
    print(pos)
    return text[:pos] + new + text[pos + len(word):]

text = "adsfhfhdsdfj"
print(replace(text, "adsf", "***"))
