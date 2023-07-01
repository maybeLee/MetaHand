# This script is used to convert COCO's label format to Darknet's

# COCO's label format: [category, x,y,width,height]
# x, y: the upper-left coordinates of the bounding box.
# width, height: the dimensions of your bounding box

# Darknet's label format: [category, x,y,width,height]
# x, y: the center coordinates of the bounding box.
# width, height: the dimensions of your bounding box
# Note that x,y,width,height are notmalized: <x> = <absolute_x> / <image_width>, 
# <height> = <absolute_height> / <image_height>
import os

WIDTH = 640
HEIGHT = 480

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
        new_x, new_y, new_width, new_height = convert_coco_to_darknet(x, y, width, height)
        new_content += f"{annotation[0]} {new_x} {new_y} {new_width} {new_height}\n"
    with open(label_path, "w") as file:
        file.write(new_content)
        
