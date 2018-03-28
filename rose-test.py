
raw=[(i, i/10) for i in range(0, 360, 10)]

from rose import Rose

r=Rose()
r.rose(raw)
r.im.save('rose.png')
