# This is the script to get the training and testing dataset, the result will be saved in training_id.txt and testing_id.txt
# Note that this file should not be run again!!!

# raise ValueError("This File SHOULD NOT BE RUN AFTER THE DATASET IS SPLITTED")
# exit()

import os

train_img_path = "./images/train/"
test_img_path = "./images/test/"

train_img_list = os.listdir(train_img_path)
test_img_list = os.listdir(test_img_path)

train_id_path = "training_id.txt"
test_id_path = "testing_id.txt"

with open(train_id_path, "a") as file:
  for img_id in train_img_list:
    if not img_id.endswith(".jpg"):
      continue
    target_path = f"/root/data_egohands/images/train/{img_id}"
    file.write(target_path+"\n")

with open(test_id_path, "a") as file:
  for img_id in test_img_list:
    if not img_id.endswith(".jpg"):
      continue
    target_path = f"/root/data_egohands/images/test/{img_id}"
    file.write(target_path+"\n")


