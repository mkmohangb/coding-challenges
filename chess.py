def solution(src, dest):
    class cell:
        def __init__(self, x=0, y=0, dist=0):
            self.x = x
            self.y = y
            self.dist = dist

    def isInside(x, y, N):
        if (x >= 0 and x <= N and
                y >= 0 and y <= N):
            return True
        return False

    def minStepToReachTarget(knightpos, targetpos, N):

        # all possible movements for the knight
        dx = [2, 2, -2, -2, 1, 1, -1, -1]
        dy = [1, -1, 1, -1, 2, -2, 2, -2]

        queue = []

        # push starting position of knight
        # with 0 distance
        queue.append(cell(knightpos[0], knightpos[1], 0))

        # make all cell unvisited
        visited = [[False for _ in range(N + 1)]
                   for _ in range(N + 1)]

        # visit starting state
        visited[knightpos[0]][knightpos[1]] = True

        count = 0
        # loop until we have one element in queue
        while len(queue) > 0:
            count += 1

            t = queue[0]
            queue.pop(0)

            # if current cell is equal to target
            # cell, return its distance
            if (t.x == targetpos[0] and
               t.y == targetpos[1]):
                return t.dist

            # iterate for all reachable states
            for i in range(8):

                x = t.x + dx[i]
                y = t.y + dy[i]

                if (isInside(x, y, N) and not visited[x][y]):
                    visited[x][y] = True
                    queue.append(cell(x, y, t.dist + 1))

    def display(visited):
        for row in visited:
            print([int(r) for r in row])

    def convert(loc):
        return [loc // 8, loc % 8]

    print(convert(src), convert(dest))
    return minStepToReachTarget(convert(src), convert(dest), 7)


print(solution(0, 1))
print(solution(19, 36))
