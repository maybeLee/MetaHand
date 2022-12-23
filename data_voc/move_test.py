import shutil
import os

target_img_dir = "/root/data_voc/images/val2014"
target_label_dir = "/root/data_voc/labels/val2014"

test_file = "/root/data_voc/testing_id.txt"

with open(test_file, "r") as file:
    content = file.read().split("\n")[:-1]

for file_path in content:
    print(f"Working on file: {file_path}")
    label_path = file_path.replace("images", "labels").replace(".jpg", ".txt")
    if not os.path.exists(file_path) or not os.path.exists(label_path):
        print("ERROR")
        break
    shutil.move(file_path, target_img_dir)
    shutil.move(label_path, target_label_dir)

