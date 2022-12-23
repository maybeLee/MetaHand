# This is the script to split training and testing dataset, the result will be saved in training_id.txt and testing_id.txt
# Note that this file should not be run again!!!

raise ValueError("This File SHOULD NOT BE RUN AFTER THE DATASET IS SPLITTED")
exit()

import os
from sklearn.model_selection import train_test_split

img_path = "./images/train2014/"
label_path = "./labels/train"

img_list = os.listdir(img_path)

train_list, test_list = train_test_split(img_list, test_size=0.2)
print(f"Total Image: {len(img_list)}, Training Image: {len(train_list)}, Testing Image: {len(test_list)}")

train_path = "training_id.txt"
test_path = "testing_id.txt"
os.system(f"rm {train_path}")
os.system(f"rm {test_path}")

with open(train_path, "a") as file:
  for img_id in train_list:
    target_path = f"/root/data_voc/images/train2014/{img_id}"
    file.write(target_path+"\n")

with open(test_path, "a") as file:
  for img_id in test_list:
    target_path = f"/root/data_voc/images/train2014/{img_id}"
    file.write(target_path+"\n")

