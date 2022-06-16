import shutil
import os
train_path = "./training_id.txt"
source_img_dir = "./coco/images"
source_label_dir = "./coco/labels"
target_dir = "/ssddata/metahand/coco2014_training"
img_list = []
label_list = []
with open(train_path, "r") as file:
    content = file.read().split("\n")[:-1]
for img_path in content:
    rel_img_path = img_path.replace("/root/data_coco/", "")
    img_list.append(rel_img_path)
    label_list.append(rel_img_path.replace("images", "labels").replace(".jpg", ".txt"))
counter = 0
assert len(img_list) == len(label_list)
for img_path, label_path in zip(img_list, label_list):
    counter += 1
    print(f"Working on image: {counter}/{len(img_list)}")
    shutil.copy(img_path, os.path.join(target_dir, "images"))
    shutil.copy(label_path, os.path.join(target_dir, "labels"))
