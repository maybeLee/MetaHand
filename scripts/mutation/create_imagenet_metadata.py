"""
This file is written to generate imagenet's metadata including:
- Creating the training_id.txt, testing_id.txt files.
- Generate labels for testing sets.
Currently, the training images/labels (288661 elements) are stored in ./data_imagenet/images and ./data_imagenet/labels.
We need to copy the testing images from data_imagenet/ILSVRC/Data/DET/val to ./data_imagenet/images_val,
We further need to create the labels for testing images using data_imagenet/ILSVRC/
"""
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import cv2
import os


SOURCE_VAL_IMG_DIR = "/root/data_imagenet/ILSVRC/Data/DET/val"
DEST_TRAIN_IMG_DIR = "/root/data_imagenet/images"
DEST_VAL_IMG_DIR = "/root/data_imagenet/images_val"
DEST_VAL_LABEL_DIR = "/root/data_imagenet/labels_val"
TRAIN_ID_PATH = "/root/data_imagenet/training_id.txt"
TEST_ID_PATH = "/root/data_imagenet/testing_id.txt"


def get_label_int_from_label_str(label_str):
    file1 = open('meta_data_for_imagenet/label.txt', 'r')
    all_lines = file1.readlines()
    get_label_int = None
    for each_line in all_lines:
        if label_str in each_line:
            if get_label_int != None:
                raise ValueError("Found duplicated label int, unhandled situation")
            get_label_int = each_line.split("(array([[")[1].split("]], dtype")[0]
            if get_label_int == None:
                raise ValueError("Split failed, something wrong")
    return get_label_int


# objective: convert bbox coordinates to x_center,y_center,width,height, so that the normalized coordinates can be processed by mutation_operation's center_to_topleft
def normalise_bbox(image_path, bbox_corr):
    img = cv2.imread(image_path)
    obj = img.copy()
    image_height = len(obj)
    image_width = len(obj[0])
    bbox_width = bbox_corr[1] - bbox_corr[0]
    bbox_height = bbox_corr[3] - bbox_corr[2]
    x_center = bbox_corr[0] + bbox_width / 2
    y_center = bbox_corr[2] + bbox_height / 2
    del obj
    return [x_center / image_width, y_center / image_height, bbox_width / image_width, bbox_height / image_height]


def create_label_file(label_path, image_path):
    tree = ET.parse(label_path)
    root = tree.getroot()
    # line_to_append_list = []
    line_to_add_to_label_file = ""
    for type_tag in root.findall('object'):
        # print(f"attr value: {type_tag.tag}")
        label_str = type_tag.find('name').text
        xmin = type_tag.find('bndbox/xmin').text
        xmax = type_tag.find('bndbox/xmax').text
        ymin = type_tag.find('bndbox/ymin').text
        ymax = type_tag.find('bndbox/ymax').text
        bbox_corr = [int(xmin), int(xmax), int(ymin), int(ymax)]
        get_label_int = get_label_int_from_label_str(label_str)
        normalised_coordinates = normalise_bbox(image_path, bbox_corr)
        line_to_add_to_label_file += f"{get_label_int} {normalised_coordinates[0]} {normalised_coordinates[1]} {normalised_coordinates[2]} {normalised_coordinates[3]}\n"
    f = open(os.path.join(DEST_VAL_LABEL_DIR, f'{label_path.split("/")[-1].replace(".xml", ".txt")}'), 'w')
    f.write(line_to_add_to_label_file)
    f.close()


def copy_image_val():
    for image_path in Path(SOURCE_VAL_IMG_DIR).rglob('*.JPEG'):
        shutil.copy(image_path.resolve(), DEST_VAL_IMG_DIR)
        create_label_file(str(image_path.resolve()).replace("Data", "Annotations").replace(".JPEG", ".xml"),
                          str(image_path.resolve()))


def write_training_testing_id(train_img_dir, test_img_dir):
    with open(TRAIN_ID_PATH, 'w') as file:
        for train_path in Path(train_img_dir).rglob('*.JPEG'):
            file.write(str(train_path.resolve()))  # resolve will get the absolute path
    with open(TEST_ID_PATH, 'w') as file:
        for test_path in Path(test_img_dir).rglob('*.JPEG'):
            file.write(str(test_path.resolve()))  # resolve will get the absolute path


if __name__ == "__main__":
    Path(DEST_VAL_IMG_DIR).mkdir(parents=True, exist_ok=True)
    Path(DEST_VAL_LABEL_DIR).mkdir(parents=True, exist_ok=True)
    copy_image_val()
    write_training_testing_id(DEST_TRAIN_IMG_DIR, DEST_VAL_IMG_DIR)
