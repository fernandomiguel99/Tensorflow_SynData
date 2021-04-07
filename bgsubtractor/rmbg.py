import cv2
import numpy as np
from bgs import bgs
import os
from tqdm import tqdm

if __name__ == "__main__":
    bgs = bgs()
    imgdirectory = "images"

    for path, dir, files in os.walk(imgdirectory):
        for file in tqdm(files, desc = 'Creating masks'):
            if file.endswith('.JPG'):
                img = cv2.imread(os.path.join(path,file))
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                alpha = bgs.find_alpha(rgb_img)
                ret, alpha = cv2.threshold(alpha,127,255,cv2.THRESH_BINARY)
                alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

                mask_name = file.replace('.JPG','.pbm')
                cv2.imwrite(os.path.join(path, mask_name), alpha)
