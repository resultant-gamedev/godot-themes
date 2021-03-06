#!/usr/bin/env python
from PIL import Image, ImageEnhance
import PIL.ImageOps
import fnmatch
import shutil
import os

def globPath(path, pattern):
    result = []
    for root, subdirs, files in os.walk(path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                result.append(os.path.join(root, filename))
    return result


def inverse(inpng, outpng):
    image = Image.open(inpng)
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = PIL.ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))
        final_transparent_image.save(outpng)
    else:
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(outpng)


def darken(inpng, outpng, darkness):
    im1 = Image.open(inpng)
    im2 = im1.point(lambda p: p * darkness)
    im2.save(outpng)


def bright(inpng, outpng, brightness):
    peak = Image.open(inpng)
    enhancer = ImageEnhance.Brightness(peak)
    bright = enhancer.enhance(brightness)
    bright.save(outpng)


def makeClone(name, brightness):
    outdir = os.path.join("..", name)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    for p in globPath('.', "**"):
        outfile = os.path.join(outdir, p)
        curdir = os.path.dirname(outfile)
        if not os.path.isdir(curdir):
            os.makedirs(curdir)
        if p.endswith(".png"):
            bright(p, outfile, brightness)
        elif p.endswith(".tres"):
            content = open(p).read()
            content = content.replace("res://addons/adobe/", "res://addons/{}/".format(name))
            of = open(outfile, 'w')
            of.write(content)
            of.close()
        else:
            shutil.copy(p, outfile)

makeClone("adobe_dark", 0.65)
makeClone("adobe_light", 1.35)
