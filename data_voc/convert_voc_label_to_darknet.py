# This script is used to convert VOC's label format to Darknet's

# VOC's label format: [category, x,y,width,height]
# x, y: the upper-left coordinates of the bounding box.
# width, height: the dimensions of your bounding box

# Darknet's label format: [category, x,y,width,height]
# x, y: the center coordinates of the bounding box.
# width, height: the dimensions of your bounding box
# Note that x,y,width,height are notmalized: <x> = <absolute_x> / <image_width>, 
# <height> = <absolute_height> / <image_height>
import os
import matplotlib.pyplot as plt
# matplotlib format: (height, width, channel)
# label format: [category, x, y, width, height] x -> width, y-> height



label_dir = "./origin_labels"
new_label_dir = "./labels/train2014"
img_dir = "./images/train2014"


def convert_coco_to_darknet(x,y,width,height, h, w):
    new_x = x + width//2
    new_y = y + height//2
    return new_x/w, new_y/h, width/w, height/h

label_list = os.listdir(label_dir)
for label in label_list:
    img_id = label[:-4]
    img_path = os.path.join(img_dir, f"{img_id}.jpg")
    img = plt.imread(img_path)
    h, w, c = img.shape
    print(f"Image ID: {img_id}, Height is: {h}, Width is: {w}")

    label_path = os.path.join(label_dir, label)
    new_label_path = os.path.join(new_label_dir, label)
    with open(label_path, "r") as file:
        content = file.read().split("\n")[:-1]
    new_content = ""
    for line in content:
        annotation = line.split(" ")
        x, y, width, height = annotation[1:]
        x, y, width, height = float(x), float(y), float(width), float(height)
        new_x, new_y, new_width, new_height = convert_coco_to_darknet(x, y, width, height, h, w)
        new_content += f"{annotation[0]} {new_x} {new_y} {new_width} {new_height}\n"
    with open(new_label_path, "w") as file:
        file.write(new_content)
        
