class Node():
    def __init__ (self, name):
        self.name = name 
        self.neighbours = []
        self.visited = False
        self.parent = ""

n, m = map(int, input().split())
nodes = {}
temp_nodes = list(input().split())
for i in temp_nodes:
    nodes[i] = Node(i)
start, end = input().split()
for i in range(m):
    a, b = input().split()
    nodes[a].neighbours.append(b)
    nodes[b].neighbours.append(a)

def BFS(graph, start, end):
    queue = [start]
    graph[start].visited = True
    while queue:
        pos = queue.pop(0)
        if pos == end:
            break
        for np in graph[pos].neighbours:
            if not graph[np].visited:
                queue.append(np)
                graph[np].visited = True
                graph[np].parent = pos

    backtrace = [end]
    pos = end
    while pos != start:
        pos = graph[pos].parent
        backtrace.append(pos)
    return backtrace

print(BFS(nodes, start, end))
