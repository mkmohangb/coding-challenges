def solution(entrances, exits, path):
    class Graph:
     
        def __init__(self, graph):
            self.graph = graph
            self.ROW = len(graph)
     
        def BFS(self, s, t, parent):
     
            visited = [False]*(self.ROW)
     
            queue = []
     
            queue.append(s)
            visited[s] = True
     
            while queue:
     
                u = queue.pop(0)
                for ind, val in enumerate(self.graph[u]):
                    if visited[ind] == False and val > 0:
                        queue.append(ind)
                        visited[ind] = True
                        parent[ind] = u
                        if ind == t:
                            return True
     
            return False
                 
         
        def FordFulkerson(self, source, sink):
     
            parent = [-1]*(self.ROW)
     
            max_flow = 0 # There is no flow initially
     
            while self.BFS(source, sink, parent) :
                path_flow = float("Inf")
                s = sink
                while(s !=  source):
                    path_flow = min (path_flow, self.graph[parent[s]][s])
                    s = parent[s]
     
                max_flow +=  path_flow
     
                v = sink
                while(v !=  source):
                    u = parent[v]
                    self.graph[u][v] -= path_flow
                    self.graph[v][u] += path_flow
                    v = parent[v]
     
            return max_flow

    source = entrances[0]
    sink = exits[0]
    if len(exits) > 1 or len(entrances) > 1:
        n = len(path)
        source = n
        sink = n+1
        max = float("inf")
        for row in range(n):
            path[row].append(0)
            path[row].append(max if row in exits else 0)

        n += 2
        path.append([(max if x in entrances else 0) for x in range(n)])
        path.append([0]*n)

    g = Graph(path)
    return g.FordFulkerson(source, sink)
  
 
path = [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]] 
path = [[0, 0, 4, 6, 0, 0], 
         [0, 0, 5, 2, 0, 0], 
         [0, 0, 0, 0, 4, 4], 
         [0, 0, 0, 0, 6, 6], 
         [0, 0, 0, 0, 0, 0], 
         [0, 0, 0, 0, 0, 0]]
exits = [3]
entrances = [0]
exits = [4,5]
entrances = [0,1]
print(solution(entrances, exits, path))
