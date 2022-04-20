import PIL
import numpy
from PIL import Image, ImageDraw
import time
import pygame
from opensimplex import OpenSimplex


def perlin(size, octaves, coords, seed):
    trueperlin = True
    delta_x, delta_y = coords
    octavelist = []
    for o in range(octaves+1, 0, -1):
        octavesize = int(size / (2**o))
        if octavesize < 1:
            break
        if trueperlin:
            os = OpenSimplex(seed) #mb take this outside of cycle??????????????????????????????????????????????????????????????????????
            heightmap = numpy.array([[128*(os.noise2d((x - delta_x)/(2**o), (y +
                                                                             delta_y)/(2**o)) + 1) for x in range(octavesize)] for y in range(octavesize)])
            # heightmap = numpy.fromfunction(noise, (octavesize, octavesize), dtype='int')
        else:
            heightmap = numpy.random.randint(
                low=0, high=256, size=(octavesize, octavesize))
        octave = Image.fromarray(heightmap).resize((size, size), 2)
        octave = numpy.asarray_chkfinite(octave)
        octavelist.append(octave)
    k = 2
    start = octavelist.pop(0)/k
    for octave in octavelist:
        k = int(k*2)
        start = start + octave/k

    normalize = True
    if normalize:
        high = 255
        low = 2
        mins = numpy.min(start)
        maxs = numpy.max(start)
        # print(f'min {int(mins)}, max {int(maxs)} BEFORE')
        rng = maxs - mins
        start = high - (((high - low) * (maxs - start)) / rng)
        # mins = numpy.min(start)
        # maxs = numpy.max(start)
        # print(f'min {int(mins)}, max {int(maxs)} AFTER')
    return numpy.int_(start)


def grad(pack):
    g = Image.new('RGB', (3, 1))
    gd = ImageDraw.Draw(g)
    for i in range(3):
        gd.point((i, 0), pack[i])
    g1 = Image.new('RGB', (len(pack)-3, 1))
    gd1 = ImageDraw.Draw(g1)
    for i in range(3, len(pack)):
        gd1.point((i-3, 0), pack[i])
    g = g.resize((180, 1), 3)
    g1 = g1.resize((255, 1), 3)
    s = (g.size[0] + g1.size[0], 1)
    g = g.tobytes('raw', 'RGB') + g1.tobytes('raw', 'RGB')
    g = Image.frombytes('RGB', s, g)
    g = g.resize((255, 1), 3)
    final = []
    for i in range(255):
        pix = g.getpixel((i, 0))
        final.append(pix)
    final = numpy.array(final)

    return final


def col(heightmap, g):
    im = Image.fromarray(heightmap).convert("RGB")
    d = ImageDraw.Draw(im)
    for y in range(numpy.size(heightmap, axis=1)):
        for x in range(numpy.size(heightmap, axis=1)):
            p = im.getpixel((x, y))
            c = g[p[0] - 1]
            d.point((x, y), tuple(c))
    return im


def gen(colorize, size, octaves, windowsize, coords, seed, gradient):
    t1 = time.time()
    heightmap = perlin(size, octaves, coords, seed)
    t2 = time.time()
    # print(f'perlin {t2-t1}')
    if colorize:
        t1 = time.time()
        heightmap = col(heightmap, gradient)
        t2 = time.time()
        # print(f'colorize {t2 - t1}')
    else:
        heightmap = Image.fromarray(heightmap)
    heightmap = heightmap.resize((windowsize, windowsize), 0)
    return heightmap


if __name__ == '__main__':
    deepwater = (39, 125, 161)
    water = (87, 117, 144)
    smallwater = (77, 144, 142)
    sand = (249, 199, 79)
    grasssand = (250, 181, 97)
    grass = (152, 210, 98)
    mountaingrass = (107, 155, 70)
    mountain = (147, 169, 154)
    hightmountain = (131, 127, 113)
    snow = (245, 238, 255)
    colorsdata = [deepwater, water, smallwater, sand,
                  grasssand, mountaingrass, mountain, hightmountain, snow]
    grd = grad(colorsdata)

    seed = numpy.random.randint(1, 10000000)
    windowsize = 700
    sc = pygame.display.set_mode(
        (windowsize, windowsize))
    delta_x = 0
    delta_y = 0
    colorize = True
    displayfps = True
    size = 128
    octaves = 4
    timetoprint = 0
    movingx = 0
    movingy = 0
    while(True):
        delta_x += 0.1
        delta_y += 0.1
        t1 = time.time()
        im = gen(colorize, size, octaves, windowsize,
                 (delta_x, delta_y), seed, grd)
        s = im.convert('RGBA').tobytes("raw", "RGBA")
        m = im.convert('RGBA').mode
        sz = im.convert('RGBA').size
        pyim = pygame.image.fromstring(s, sz, m)
        sc.blit(pyim, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit(0)
        t2 = time.time()
        if displayfps:
            if timetoprint % 24 == 0:
                print(f'avg framerate {int(1/(t2-t1))}')
                timetoprint = 1
                calls = 0
            else:
                timetoprint += 1


'''
OLD GRAD:
    #import colour
    # colorsdata = []
    # for c in pack:
    #     c1, c2, c3 = c
    #     c1 /= 255
    #     c2 /= 255
    #     c3 /= 255
    #     c = (c1, c2, c3)
    #     colorsdata.append(c)
    # clist = []
    # grads = []
    # prefinal = []
    # final = []
    # for c in colorsdata:
    #     clist.append(colour.Color(rgb=c))
    # for i in range(1, len(colorsdata)):
    #     # g = list(clist[i - 1].range_to(clist[i], steps=29))
    #     g = list(colour.color_scale(colour.rgb2hsl(colorsdata[i - 1]), colour.rgb2hsl(colorsdata[i]), 26))
    #     grads.append(g)
    # for g in grads:
    #     g = [colour.hsl2rgb(gi) for gi in g]
    #     prefinal += g
    # while len(prefinal) > 255:
    #     prefinal.pop()
    # for c in prefinal:
    #     c1, c2, c3 = c#.rgb
    #     new = (int(c1*255), int(c2*255), int(c3*255))
    #     final.append(new)
'''
