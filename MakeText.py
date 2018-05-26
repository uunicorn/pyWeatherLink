import PIL.ImageFont
import PIL.Image
import PIL.ImageDraw

font = PIL.ImageFont.truetype(filename='/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf', size=25)
line_spacing = 5


def make_text(text):
    lines = text.split('\n')

    max_x=0
    total_y=0

    for line in lines:
        x, y = font.getsize(line)
        if x > max_x:
            max_x = x
        total_y = total_y + y + line_spacing

    im = PIL.Image.new(mode='RGBA', size=(max_x, total_y))
    draw = PIL.ImageDraw.ImageDraw(im)
    draw.setfont(font)

    total_y=0
    for line in lines:
        x, y = font.getsize(line)
        draw.text(xy=(0, total_y), text=line, fill=(0,0,0,255))
        total_y = total_y + y + line_spacing

    return im

