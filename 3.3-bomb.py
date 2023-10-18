def solution(x, y):
    def is_solvable(x, y):
        return x > 0 and y > 0 and x != y

    x, y = int(x), int(y)
    steps = 0
    while (is_solvable(x, y)):
        cur_step = 0
        if x > y:
            if x % y == 0:
                cur_step = -1
            cur_step += x // y
            x = x - y * cur_step
            steps += cur_step
        elif y > x:
            if y % x == 0:
                cur_step = -1
            cur_step += y // x
            y = y - x * cur_step
            steps += cur_step
        else:
            break

    if x == 1 and y == 1:
        return str(steps)
    else:
        return "impossible"


print("solution is ", solution('2', '1'))
print("solution is ", solution('4', '7'))
print("solution is ", solution('2', '4'))
