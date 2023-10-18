def solution(start, length):

    def xor_range(a, b):
        def f(x):
            res = [x, 1, x + 1, 0]
            return res[x % 4]
        return f(b) ^ f(a-1)
    chksum = 0
    for i in range(length):
        res = xor_range(start, start + length - i - 1)
        chksum ^= res
        start += length
        print()
    print()
    return chksum


print("solution is ", solution(1, 1))
print("solution is ", solution(0, 3))
print("solution is ", solution(17, 4))
print("solution is ", solution(10, 5))
