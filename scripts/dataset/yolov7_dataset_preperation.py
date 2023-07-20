# Prepare the training/validation dataset in a format that can be accepted by yolov7
# input: path of all images (e.g., ./images), path of all labels (e.g., ./labels)
# output: the following dataset directory structure
"""
./
├── images
│ ├── train (80%)
│ └── val (20%)
├── labels
│ ├── train
│ └── val
├── train.txt
└── val.txt
└── data.yaml
"""

import os
import random
import shutil
import sys
import argparse

random.seed(1234)


def split_train_val(img_dir, dest_dir):
    # Set the percentage of images to use for the validation set
    val_percent = 0.2

    # Create the directories for the training and validation sets
    train_img_dir = os.path.join(dest_dir, "images", "train")
    val_img_dir = os.path.join(dest_dir, "images", "val")

    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    # prepare the label directory
    img_tag = os.sep + "images" + os.sep  # "/images/"
    label_tag = os.sep + "labels" + os.sep  # "/labels/"
    os.makedirs(train_img_dir.replace(img_tag, label_tag, 1), exist_ok=True)
    os.makedirs(val_img_dir.replace(img_tag, label_tag, 1), exist_ok=True)

    # Get the list of image filenames in the image directory
    image_filenames = os.listdir(img_dir)
    num_images = len(image_filenames)

    # Calculate the number of images to use for the validation set
    num_val_images = int(num_images * val_percent)

    # Shuffle the list of image filenames randomly
    random.shuffle(image_filenames)

    def copy_img_label(img_name, dst_dir):
        src_path = os.path.join(img_dir, img_name)
        dst_path = os.path.join(dst_dir, img_name)
        # copy image
        shutil.copy(src_path, dst_path)
        # copy label
        shutil.copy(
            'txt'.join(src_path.replace(img_tag, label_tag, 1).rsplit(src_path.split('.')[-1], 1)),
            'txt'.join(dst_path.replace(img_tag, label_tag, 1).rsplit(dst_path.split('.')[-1], 1)),
        )
        return dst_path


    # Copy the first num_val_images images to the validation set directory
    val_img_paths = []
    for i in range(num_val_images):
        img_path = copy_img_label(image_filenames[i], val_img_dir)
        val_img_paths.append(img_path.replace(dest_dir, "./"))

    train_img_paths = []
    # Copy the remaining images to the training set directory
    for i in range(num_val_images, num_images):
        img_path = copy_img_label(image_filenames[i], train_img_dir)
        train_img_paths.append(img_path.replace(dest_dir, "./"))

    # Save the paths of the training and validation images to separate text files
    with open(os.path.join(dest_dir, "train.txt"), "w") as f:
        for path in train_img_paths:
            f.write(path + "\n")

    with open(os.path.join(dest_dir, "val.txt"), "w") as f:
        for path in val_img_paths:
            f.write(path + "\n")

    # add yaml file
    with open(os.path.join(dest_dir, "data.yaml"), "w") as f:
        """
            train: ./pilotstudy/train.txt  # images
            val: ./pilotstudy/val.txt  # images

            # number of classes
            nc: 1

            # class names
            names: [ 'hand']
        """
        f.write(
            f"train: {os.path.join(dest_dir, 'train.txt')}\n"
            f"val: {os.path.join(dest_dir, 'val.txt')}\n"
            f"nc: 1\n"
            f"names: [ 'hand' ]\n"
            f""
        )


def run(img_dir, label_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    assert img_dir.replace("images", "labels", 1) == label_dir
    split_train_val(img_dir, dest_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_img_dir", type=str, default="./data_pilot/images", help="the directory of images")
    parser.add_argument("--src_label_dir", type=str, default="./data_pilot/labels", help="The directory of labels")
    parser.add_argument("--target_dir", type=str, default="./tools/yolov7/pilotstudy", help="The destination of data")
    flags, _ = parser.parse_known_args(sys.argv[1:])
    run(flags.src_img_dir, flags.src_label_dir, flags.target_dir)
