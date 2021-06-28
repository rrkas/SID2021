l = list(map(int, input('Enter comma separated integers: ').split(',')))
t = int(input('target: '))

res = []

if len(l) < 3:
    print('No triplets')
    exit()

if sum(l) < t:
    print('No triplets')
    exit()

for i in range(len(l)-2):
    for j in range(i+1, len(l)-1):
        for k in range(j+1, len(l)):
            v = [l[i], l[j], l[k]]
            if sum(v) == t:
                res.append(v)

print(res)