def solution(n, b):
    def numberToBase(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return ''.join(map(str, digits[::-1]))
    k = len(n)
    ids = []
    length = 1
    while len(n) > 1:
        x = "".join(sorted([i for i in n], reverse=True))
        y = "".join(sorted([i for i in n], reverse=False))
        print(x, y)
        print(int(x, b))
        print(int(y, b))
        z = int(x, b) - int(y, b)
        if b != 10:
            z = numberToBase(z, b)
        n = str(z).zfill(k)
        if n in ids:
            length = len(ids) - ids.index(n)
            break
        ids.append(n)
        print(z)
    return length


print("solution is ", solution("1211", 10))
print("solution is ", solution("41", 10))
print("solution is ", solution("11", 10))
print("solution is ", solution("210022", 3))
