from __future__ import print_function
import PIL
import numpy
from PIL import Image, ImageDraw
import colour


def perlin(size=100, octaves=5):
    octavelist = []
    for o in range(octaves+1, 0, -1):
        octavesize = int(size / (2**o))
        if octavesize < 1:
            break
        heightmap = numpy.random.randint(
            low=0, high=256, size=(octavesize, octavesize))
        octave = Image.fromarray(heightmap).resize((size, size), 3)
        octave = numpy.asarray_chkfinite(octave)
        octavelist.append(octave)
    k = 2
    start = octavelist.pop(0)/k
    for octave in octavelist:
        k = int(k*2)
        start = start + octave/k
    return numpy.int_(start)


def grad(pack):
    colorsdata = []
    for c in pack:
        c1, c2, c3 = c
        c1 /= 255
        c2 /= 255
        c3 /= 255
        c = (c1, c2, c3)
        colorsdata.append(c)
    clist = []
    grads = []
    prefinal = []
    final = []
    for c in colorsdata:
        clist.append(colour.Color(rgb=c))
    for i in range(1, len(clist)):
        g = list(clist[i - 1].range_to(clist[i], steps=29))
        grads.append(g)
    for g in grads:
        prefinal += g
    while len(prefinal) > 255:
        prefinal.pop()
    for c in prefinal:
        c1, c2, c3 = c.rgb
        new = (int(c1*255), int(c2*255), int(c3*255))
        final.append(new)
    final = numpy.array(final)
    return final


def col(heightmap, colorsdata):
    g = grad(colorsdata)
    im = Image.fromarray(heightmap).convert("RGB")
    d = ImageDraw.Draw(im)
    print('gradient len: ', len(g))
    for y in range(numpy.size(heightmap, axis=1)):
        for x in range(numpy.size(heightmap, axis=1)):
            p = im.getpixel((x, y))
            c = g[p[0]]
            d.point((x, y), tuple(c))
    return im


if __name__ == '__main__':
    heightmap = perlin(800, 5)
    deepwater = (0, 52, 222)
    water = (0, 125, 222)
    smallwater = (0, 203, 222)
    grasssand = (222, 215, 0)
    sand = (173, 223, 0)
    grass = (41, 223, 0)
    mountaingrass = (94, 160, 23)
    mountain = (131, 107, 23)
    hightmountain = (175, 175, 175)
    snow = (255, 255, 255)
    colorsdata = [deepwater, water, smallwater, sand, grasssand,
                  grass, mountaingrass, mountain, hightmountain, snow]
    col(heightmap, colorsdata).resize((800, 800)).show()
    # heightmap = numpy.array([[255 * random.random() for i in range(3)] for j in range(3)])
    # heightmap[0][0] = 0
    # octave = Image.fromarray(heightmap, 'L').resize((4, 4), 2)
    # octave.resize((400, 400), 2).show()
    # print(heightmap)
    # heightmap = numpy.asarray_chkfinite(octave)
    # print(heightmap)
