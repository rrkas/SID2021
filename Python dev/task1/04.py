l = list(map(int,input('Enter list of numbers separated by ,: ').split(',')))

def gcd(a, b):
    if b > a:
        a, b = b, a
    if(b == 0):
        return a
    else:
        return gcd(b, a % b)

if len(l) == 0:
    print(0)
elif len(l) == 1:
    print(l[0])
else:
    g = gcd(l[0], l[1])
    for i in range(2, len(l)):
        g = gcd(g, l[i])
    print(g)