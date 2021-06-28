n = int(input())

c = 0
l = []
t = 1
while c < n:
    s = 0
    for i in range(1, t):
        if t % i==0:
            s += i
    if s==t:
        c += 1
        l.append(t)
    t += 1

print(*l, sep=',')
