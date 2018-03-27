# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageShow, ImagePath
from matrix import *
from math import ceil

Image.init()

def radial2xy(ad):
    return apply((0, ad[1]), rotate(ad[0]))

class Rose(object):
    def __init__(self):
        size=(400, 400)
        rose_radius=170
        self.fatness = 5

        transform=id
        transform=compose(scale(rose_radius, -rose_radius), transform)
        transform=compose(offset(size[0]/2, size[1]/2), transform)
        self.transform = transform

        self.im = Image.new('RGBA', size, (0,0,0,0))

    def dot(self, xy):
        m = scale(self.fatness, self.fatness)
        m = compose(offset(xy[0], xy[1]), m)
        bounds = [(-1, -1), (1, 1)]
        bounds = [apply(xy, m) for xy in bounds]
        return bounds

    def paint(self, im, frm, to):
        line = [frm, to]
        line = [radial2xy(ad) for ad in line]
        line = [apply(xy, self.transform) for xy in line]

        r, g, b, a = im.split()
        a = Image.eval(a, lambda x: x/1.2)
        im = Image.merge('RGBA', (r, g, b, a))
        draw = ImageDraw.ImageDraw(im)
        draw.line(line, fill=(255, 0, 0, 255), width=2)
        draw.ellipse(self.dot(line[1]), fill=(255, 0, 0, 255))
        return im

    def circle(self, r, txt):
        bounds = [(-r, r),(r,-r)]
        bounds = [apply(xy, self.transform) for xy in bounds]
        self.draw.ellipse(bounds, outline=(128, 128, 128, 255))
        xy = apply((0, r), self.transform)
        ts = self.draw.textsize(txt)
        xy = tuple([a - b/2 for (a, b) in zip(xy, ts)])
        self.draw.text(xy, txt, fill=(0, 0, 0, 255))

    def dir(self, angle, txt):
        m = compose(self.transform, rotate(angle))
        # draw direction tick
        line = [(0, 1), (0, 0.9)]
        line = [apply(xy, m) for xy in line]
        self.draw.line(line, fill=(128, 128, 128, 255))
        # draw text
        # transform coordinates for text
        text = apply((0, 1.1), m)
        # adjst for text box size
        ts = self.draw.textsize(txt)
        text = tuple([a - b/2 for (a, b) in zip(text, ts)])
        self.draw.text(text, txt, fill=(0, 0, 0, 255))

    def rose(self, raw):
        self.max_kn = ceil(max([1] + [i[1] for i in raw])/5)*5
        raw = [(dir*pi/180, kn/self.max_kn) for (dir, kn) in raw if dir and kn]
        last = raw[0]

        for data in raw[1:]:
            self.im = self.paint(self.im, last, data)
            last = data
        
        self.grid()

    def grid(self):
        self.draw = ImageDraw.ImageDraw(self.im)

        for r in range(1, 6):
            self.circle(r/5.0, "%d" % (self.max_kn*r/5))

        for a in range(0, 360, 45):
            self.dir(a*pi/180, "%03d" % a)

