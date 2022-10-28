#!/usr/bin/env python
# Create train.txt and val.txt containing paths for all train and val images
# Create labels/image_id.txt containing labels for each image in train.txt. Images without labels are excluded
# Populate image folder with dummy images when debug option is passed


import pandas as pd
from sklearn.model_selection import StratifiedKFold
from shapely.wkt import loads
import numpy as np
import sys
import subprocess
import random
import cv2
from pathlib import Path



if __name__=="__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument(
        "--debug",
        action='store_true',
        help="Create a dataset for debuging"
    )
    
    args = arg.parse_args()
    debug = args.debug
    if len(args) > 0:
        option = args[0]
        debug = option == "debug"
    
    bboxes_df = pd.read_csv("data/images_bboxes.csv")
    train_df = pd.read_csv("data/Train.csv")
    test_df = pd.read_csv("data/Test.csv")
    bbox_df = pd.read_csv("data/images_bboxes.csv")

    labels_dir = Path("data/labels")
    images_dir = Path("data/images")
    train_labels_dir = labels_dir/"train"
    val_labels_dir = labels_dir/"val"
    train_images_dir = images_dir/"train"
    val_images_dir = images_dir/"val"
    test_images_dir = images_dir/"test"

    # only rows with objects
    train_df = train_df.loc[train_df["number_of_worms"]!=0]

    # train.txt
    train_txt = Path("data/train.txt")
    val_txt = Path("data/val.txt")

    image_names = train_df["image_id_worm"].value_counts().index.values
    types_present = train_df["image_id_worm"].value_counts().values

    skf = StratifiedKFold(n_splits=10)
    for train_idx, val_idx in skf.split(image_names, types_present):
        train_names = image_names[train_idx].tolist()
        val_names = image_names[val_idx].tolist()
        break

    # labels
    def _write_labels(image_names, txt, labels_dir, dest_images_dir):
        num_names = len(image_names) if not debug else 120
        worm_type_idx = {"pbw":0, "abw":1}
        if debug:
            color_map = [[255, 0, 255], [0, 255, 255]]
        for i,name in enumerate(train_names):
            with open(txt, "a") as f:
                f.write(f"../data/images/{name}\n")
            with open(labels_dir/f"{name.split('.')[0]}.txt", "w") as f:
                if (images_dir/name).exists():
                    subprocess.Popen(["mv", f"{images_dir/name}", f"{dest_images_dir/name}"]).wait()
                df = bbox_df[bbox_df["image_id"] == name]
                if debug:
                    w = 2000
                    h = 2000
                    image = np.zeros((h,w,3), dtype=np.uint8)
                else:
                    w,h,_ = cv2.imread((dest_images_dir/name).str).shape
                for worm_type, geometry in zip(df["worm_type"].values, df["geometry"].values):
                    clsidx = worm_type_idx[worm_type]
                    x1,y1,x2,y2 = loads(geometry).bounds
                    if debug:
                        x1 = random.randint(10, w-110)
                        y1 = random.randint(10, h-110)
                        x2 = x1 + 100
                        y2 = y1 + 100
                        image[y1:y2, x1:x2] = color_map[clsidx]
                        cv2.imwrite(f"{dest_images_dir/name}", image)    
                    
                    w_ = (x2-x1+1)
                    h_ = (y2-y1+1)
                    c_x = (x1 + w_/2)/w
                    c_y = (y1 + h_/2)/h
                    w_ = w_/w
                    h_ = h_/h
                    
                    f.write(f"{clsidx} {c_x} {c_y} {w_} {h_}\n")
                
                if debug and i >= 120:
                    break
                prog = min(50, int(50*(i+1)/num_names))
                print(f"{100*(i+1)/num_names:4.2f}% [ {'>'*prog}{'-'*(50-prog)} ]", end="\r")
        print(f"{100*(i+1)/num_names:4.2f}% [ {'>'*prog}{'-'*(50-prog)} ]")
                
                  
    # train labels
    print("writing train labels")
    _write_labels(train_names, train_txt, train_labels_dir, train_images_dir)

    # val labels
    print("writing val labels")
    _write_labels(val_names, val_txt,val_labels_dir, val_images_dir)