import os

WIDTH = 640
HEIGHT = 480

label_dir = "../../data_coco/Labels"

label_list = os.listdir(label_dir)
category_list = []
for label in label_list:
    label_path = os.path.join(label_dir, label)
    with open(label_path, "r") as file:
        content = file.read().split("\n")[:-1]
    new_content = ""
    for line in content:
        annotation = line.split(" ")
        category = int(annotation[0])
        if category not in category_list:
            category_list.append(category)

category_list.sort()
print(category_list)