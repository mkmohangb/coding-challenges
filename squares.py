import sys


def solution(area):
    def get_largest_square(area):
        largest = 0
        if area == 1:
            return 1
        for i in range(area//2 + 1):
            cur = i * i
            # print(cur, area, largest)
            if cur > largest and cur <= area:
                largest = cur
            if cur > area:
                break
        return largest

    squares = []
    while area > 0:
        largest = get_largest_square(area)
        squares.append(largest)
        area -= largest
    return squares


area = int(sys.argv[1])
print(solution(area))
