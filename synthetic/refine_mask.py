#!/usr/bin/python
#!coding: utf-8
import os
import argparse
import cv2
import numpy as np
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        'Refine all images masks in a folder and subfolders',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Example usage:
    python {0} -i /home/user/example/Images/Masks'''.format(__file__))
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help=
        'Path to the masks to be refined'
    )

    args = parser.parse_args()
    input = args.input

    for path, dir, files in tqdm(os.walk(input), desc ='Refining masks'):
        for file in files:
            if file.endswith('.pbm'):
                im = cv2.imread(os.path.join(path,file), 0)
                blur = cv2.blur(im,(15,15))
                ret, thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                kernel = np.ones((21,21),np.uint8)
                closing = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel, iterations = 3)
                os.remove(os.path.join(path, file))
                cv2.imwrite(os.path.join(path,file), closing)
