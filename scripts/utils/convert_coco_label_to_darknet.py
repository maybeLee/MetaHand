# This script is used to convert COCO's label format to Darknet's

# COCO's label format: [category, x,y,width,height]
# x, y: the upper-left coordinates of the bounding box.
# width, height: the dimensions of your bounding box

# Darknet's label format: [category, x,y,width,height]
# x, y: the center coordinates of the bounding box.
# width, height: the dimensions of your bounding box
# Note that x,y,width,height are normalized: <x> = <absolute_x> / <image_width>,
# <height> = <absolute_height> / <image_height>
import os

WIDTH = 640
HEIGHT = 480
coco_category = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17,
                 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 31, 32, 33, 34,
                 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49,
                 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
                 64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
                 82, 84, 85, 86, 87, 88, 89, 90]

label_dir = "../../data_coco/Labels"

def convert_coco_to_darknet(x,y,width,height):
    new_x = x + width//2
    new_y = y + height//2
    return new_x/WIDTH, new_y/HEIGHT, width/WIDTH, height/HEIGHT

label_list = os.listdir(label_dir)
for label in label_list:
    label_path = os.path.join(label_dir, label)
    with open(label_path, "r") as file:
        content = file.read().split("\n")[:-1]
    new_content = ""
    for line in content:
        annotation = line.split(" ")
        x, y, width, height = annotation[1:]
        class_id = int(annotation[0])
        new_x, new_y, new_width, new_height = convert_coco_to_darknet(float(x), float(y), float(width), float(height))
        new_content += f"{coco_category.index(class_id)} {new_x} {new_y} {new_width} {new_height}\n"
    with open(label_path, "w") as file:
        file.write(new_content)
        
