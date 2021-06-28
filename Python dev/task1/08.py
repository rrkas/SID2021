n = int(input())

for i in range(2*n):
    if i < n:
        print(' ' * i , end='')
        print('* '*(n-i))
    elif i == n:
        continue
    else:
        print(' ' * (2*n-i-1) , end='')
        print('* '*((i-n+1)))