#!/usr/bin/python
#!coding: utf-8
import os
import argparse
from tqdm import tqdm
import mmap

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        'Look up for images in a directory and subdirectories and rename all the images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Example usage:
    python {0} -i /home/user/example/images '''.format(__file__))
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help=
        'Path to look up for images.'
    )

    args = parser.parse_args()
    indirectory = args.input

    for path, dir, files in os.walk(indirectory):
        i = 1
        for file in tqdm(files, desc = 'Processing class {0}'.format(path.split('/')[-1])):
            if file.endswith('.png') or file.endswith('.jpg'):
                dir_names = path.split("/")
                new_name = dir_names[-1]+'_'+str(i)+'.jpg'
                os.rename(os.path.join(path, file), os.path.join(path, new_name))
                i += 1
