def caesar(text, shift):
    shift = shift % 26
    result = ""
    for letter in text:
        if letter.isalpha() == False:
            result += letter
            continue
        
        new = ord(letter) + shift
        if letter.isupper():
            if new > ord('Z'):
                new -= 26
            if new < ord('A'):
                new += 26
        else:
            if new > ord('z'):
                new -= 26
            if new < ord('a'):
                new += 26

        result += chr(new)
    return result

print(caesar("abcABC", -3))
