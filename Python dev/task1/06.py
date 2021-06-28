s = input('s: ')
f = input('f: ')

c = 0
for i in range(len(s)):
    if s[i:].startswith(f):
        c += 1

print(c)