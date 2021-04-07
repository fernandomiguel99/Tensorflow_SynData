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
        'Split .txt files in a folder in train-test',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Example usage:
    python {0} -i /home/user/example/Labels -f 0.8'''.format(__file__))
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help=
        'Path to the labels to be splited'
    )
    parser.add_argument(
        '-f',
        '--fraction',
        type=float,
        help=
        'Train fraction'
    )

    args = parser.parse_args()
    directory = args.input
    frac = args.fraction

    for path, dir, files in os.walk(directory):
        for file in tqdm(files, desc = 'Spliting files'):
            if file.endswith('.txt'):
                
