
from math import cos, sin, pi

id=(1, 0, 0,
    0, 1, 0)

def scale(x, y):
    return (x, 0, 0,
            0, y, 0)
def offset(x, y):
    return (1, 0, x,
            0, 1, y)

def rotate(a):
    return (cos(a),  sin(a), 0,
            -sin(a), cos(a), 0)

lastrow=(0, 0, 1)
indeces=[0, 1, 2]

def row(m, i):
    return [m[3*i + j] for j in indeces]

def col(m, j):
    return [m[3*i + j] for i in indeces]

def mac(a, b):
    return sum([l*r for (l, r) in zip(a, b)])

def mul(a, b):
    return [mac(row(a, i), col(b, j)) for i in indeces for j in indeces]

def compose(a, b):
    return tuple(mul(a+lastrow, b+lastrow)[:6])

def apply(xy, m):
    return (xy[0]*m[0] + xy[1]*m[1] + m[2],
            xy[0]*m[3] + xy[1]*m[4] + m[5])

