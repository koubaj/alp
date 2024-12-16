points = list(map(float, input().split()))
n = int(len(points) / 2)
x = []
y = []
for i in range(n):
    x.append(points[i*2])
    y.append(points[i*2+1])\

cx = 0
cy = 0
for i in x:
    cx += i / n
for i in y:
    cy += i / n
    
def dist(x, y, a, b):
    return abs(((x - a)**2 + (y - b)**2)**(1/2))

min_dist = dist(cx, cy, points[0], points[1])
min_index = 0
for i in range(n):
    d = dist(cx, cy, points[i*2], points[i*2+1])
    if d < min_dist:
        min_dist = d
        min_index = i

points = []
for i in range(n):
    d = dist(0, 0, x[i], y[i])
    points.append([d, x[i], y[i], i])
points.sort()
print(min_index, points[int(n/2) - 1][3])
