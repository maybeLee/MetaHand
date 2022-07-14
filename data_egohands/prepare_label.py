# gather all egohands' label into labels directory
import os
import shutil


label_dir = "./labels"
if not os.path.exists(label_dir):
  os.makedirs(label_dir)
img_dir = "./images"

def get_files(target_dir, end_pattern):
    # input: root path of specific frameworks
    # output: list format: ["file_dir_1", "file_dir_2", ...]
    # function, go through all files in the framework and only find python files
    file_lists = []
    for root, subdirs, files in os.walk(target_dir):
        for file in files:
            if not file.endswith(end_pattern):
                continue
            file_lists.append(os.path.join(root, file))
    return file_lists

label_lists = get_files(img_dir, ".txt")
for label in label_lists:
  if "README" in label:
    continue
  write_content = ""
  with open(label, "r") as file:
    for line in file:
      write_content += "0" + line[1:]
  with open(label, "w") as file:
    file.write(write_content)
    
  shutil.copy(label, label_dir)

