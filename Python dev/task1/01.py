s = input()

t = ""

for i in s:
    if i.isalpha:
        if i.islower():
            t += i.upper()
        else:
            t += i.lower()
    else:
        t += i

print(t)