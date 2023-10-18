def solution(n):
    n = int(n)
    steps = 0
    while n > 1:
        print(n, end="\t")
        steps += 1
        if n % 2 == 0:
            n //= 2
        else:
            if n == 3:
                n -= 1
            elif ((n + 1)/2) % 2 == 0:
                n += 1
            else:
                n -= 1
    print()
    return steps


print("solution is ", solution('4'))
print("solution is ", solution('15'))
print("solution is ", solution('21'))
print("solution is ", solution('23'))
print("solution is ", solution('25'))
