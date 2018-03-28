# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageShow, ImagePath
from math import ceil
from planar import Vec2, Affine

Image.init()

def vec2tuple(v):
    return (v.x, v.y)

class Rose(object):
    def __init__(self):
        size=(400, 400)
        rose_radius=170
        self.fatness = 5

        transform=Affine.identity()
        transform=Affine.scale(Vec2(rose_radius, -rose_radius))*transform
        transform=Affine.translation(Vec2(size[0]/2, size[1]/2))*transform
        self.transform = transform

        self.im = Image.new('RGBA', size, (0,0,0,0))

    def dot(self, xy):
        m = Affine.scale(Vec2(self.fatness, self.fatness))
        m = Affine.translation(Vec2(xy[0], xy[1]))*m
        bounds = [Vec2(-1, -1), Vec2(1, 1)]
        bounds = [xy*m for xy in bounds]
        return bounds

    def paint(self, im, frm, to):
        line = [frm, to]
        line = [Vec2.polar(90-ad[0], ad[1]) for ad in line]
        line = [vec2tuple(xy*self.transform) for xy in line]

        r, g, b, a = im.split()
        a = Image.eval(a, lambda x: x/1.2)
        im = Image.merge('RGBA', (r, g, b, a))
        draw = ImageDraw.ImageDraw(im)
        draw.line(line, fill=(255, 0, 0, 255), width=2)
        draw.ellipse([vec2tuple(xy) for xy in self.dot(line[1])], fill=(255, 0, 0, 255))
        return im

    def circle(self, r, txt):
        bounds = [Vec2(-r, r), Vec2(r,-r)]
        bounds = [vec2tuple(xy*self.transform) for xy in bounds]
        self.draw.ellipse(bounds, outline=(128, 128, 128, 255))
        xy = Vec2(0, r)*self.transform
        ts = self.draw.textsize(txt)
        xy = tuple([a - b/2 for (a, b) in zip(vec2tuple(xy), ts)])
        self.draw.text(xy, txt, fill=(0, 0, 0, 255))

    def dir(self, angle, txt):
        m = self.transform*Affine.rotation(angle)
        # draw direction tick
        line = [Vec2(0, 1), Vec2(0, 0.9)]
        line = [vec2tuple(xy*m) for xy in line]
        self.draw.line(line, fill=(128, 128, 128, 255))
        # draw text
        # transform coordinates for text
        text = Vec2(0, 1.1)*m
        # adjst for text box size
        ts = self.draw.textsize(txt)
        text = tuple([a - b/2 for (a, b) in zip(vec2tuple(text), ts)])
        self.draw.text(text, txt, fill=(0, 0, 0, 255))

    def rose(self, raw):
        self.max_kn = ceil(max([1] + [i[1] for i in raw])/5)*5
        raw = [(dir, kn/self.max_kn) for (dir, kn) in raw if dir and kn]
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
            self.dir(a, "%03d" % a)

