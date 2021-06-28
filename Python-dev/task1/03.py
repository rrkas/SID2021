def is_prime(n):
    if n < 0:
        return False
    elif n in [0, 1]:
        return False
    elif n in [2, 3]:
        return True
    else:
        for i in range(2, n//2+1):
            if n%i==0:
                return False
        return True


n = int(input())

l = []

for i in range(1, n+1):
    if is_prime(i):
        l.append(i)

print(*l, sep=',')