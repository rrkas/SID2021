l = list(map(int, input('Enter comma separated integers: ').split(',')))
n = int(input('Enter number: '))
l.sort()
if n < len(l):
    print(l[n-1])
else:
    print('Out of index!')