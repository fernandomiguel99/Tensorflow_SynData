#!/usr/bin/python
#!coding: utf-8
import os
import argparse
import shutil
from PIL import Image
from tqdm import tqdm
import mmap

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        'Convert all images in a folder from .png to .jpg format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Example usage:
    python {0} -img /home/user/example/Images'''.format(__file__))
    parser.add_argument(
        '-img',
        '--images',
        type=str,
        help=
        'Path to the images to be converted'
    )

    args = parser.parse_args()
    imgdirectory = args.images

    for path, dir, files in os.walk(imgdirectory):
        for file in tqdm(files, desc = 'Converting images'):
            if file.endswith('.png'):
                im = Image.open(os.path.join(path,file)).convert("RGBA")
                bg = Image.new('RGB', im.size, (255,255,255))
                x, y = im.size
                bg.paste(im, (0,0,x,y), im)
                bg.save(os.path.join(path, file.replace('png','jpg')), quality = 100)
                os.remove(os.path.join(path,file))
