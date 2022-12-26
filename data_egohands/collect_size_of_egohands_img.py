import os
import cv2


for img in os.listdir("./images/train/"):
    if not img.endswith("jpg"):
        continue
    print(cv2.imread(f"./images/train/{img}").shape)

