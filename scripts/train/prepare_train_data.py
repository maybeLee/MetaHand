import os
from sklearn.model_selection import train_test_split
from scripts.utils.logger import Logger
from scripts.utils.utils import get_files
import glob
import shutil
import argparse
import sys
logger = Logger()


class PreTrainData(object):
    def __init__(self, flags):
        self.data_path = flags.source_path
        self.img_list = []
        self.target_dir = flags.target_dir
        self.img_dir = flags.img_dir
        self.label_dir = flags.label_dir
        self.obj_dir = os.path.join(self.target_dir, "obj")
        self.backup_dir = os.path.join(self.target_dir, "backup")
        self.train_path = os.path.join(self.target_dir, "train.txt")
        self.valid_path = os.path.join(self.target_dir, "valid.txt")
        self.test_path = os.path.join(self.target_dir, "test.txt")
        self.initiate_dirs()

    def initiate_dirs(self):
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        if not os.path.exists(self.obj_dir):
            os.makedirs(self.obj_dir)
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def load_data(self):
        with open(self.data_path, "r") as file:
            content = file.read().split("\n")[:-1]
        for line in content:
            self.img_list.append(line)
        if self.data_path != "./data/training_id.txt":
            with open("./data/training_id.txt", "r") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                self.img_list.append(line)

    def _split_train_valid_test(self):
        train_list, valid_list = train_test_split(self.img_list, test_size=0.2)
        return train_list, valid_list

    def prepare_darknet_data(self):
        train_list, valid_list = self._split_train_valid_test()
        test_list = []
        with open("./data/testing_id.txt", "r") as file:
            content = file.read().split("\n")[:-1]
            for line in content:
                test_list.append(line)

        def _prepare_img_label(id: str):
            file_list = get_files(self.img_dir, f"{id}.jpg")
            label_list = get_files(self.label_dir, f"{id}.txt")
            assert len(file_list) == len(label_list) == 1
            file_path = file_list[0]
            label_path = label_list[0]
            target_file_path = os.path.join(self.obj_dir, f"{id}.jpg")
            target_label_path = os.path.join(self.obj_dir, f"{id}.txt")
            os.system(f"cp {file_path} {target_file_path}")
            os.system(f"cp {label_path} {target_label_path}")
            return target_file_path

        os.system(f"find {self.img_dir} -name '*.jpg' -exec cp " + "{}" + f" {self.obj_dir} \\;")
        os.system(f"find {self.label_dir} -name '*.txt' -exec cp " + "{}" + f" {self.obj_dir} \\;")
        os.system(f"find ./data/ImageSet/ -name '*.jpg' -exec cp " + "{}" + f" {self.obj_dir} \\;")
        os.system(f"find ./data/Labels/ -name '*.txt' -exec cp " + "{}" + f" {self.obj_dir} \\;")
        with open(self.train_path, "w") as file:
            for train_id in train_list:
                # target_file_path = _prepare_img_label(train_id)
                target_file_path = os.path.join(self.obj_dir, f"{train_id}.jpg")
                file.write(target_file_path+"\n")
        with open(self.valid_path, "w") as file:
            for valid_id in valid_list:
                # target_file_path = _prepare_img_label(valid_id)
                target_file_path = os.path.join(self.obj_dir, f"{valid_id}.jpg")
                file.write(target_file_path+"\n")
        with open(self.test_path, "w") as file:
            for test_id in test_list:
                # target_file_path = _prepare_img_label(test_id)
                target_file_path = os.path.join(self.obj_dir, f"{test_id}.jpg")
                file.write(target_file_path+"\n")
        logger.info(f"Total Number of Training Set: {len(train_list)}")
        logger.info(f"Total Number of Validation Set: {len(valid_list)}")
        logger.info(f"Total Number of Test Set: {len(test_list)}")
        for file_path in glob.glob(f"{self.obj_dir}/*.txt"):
            write_content = ""
            with open(file_path, "r") as file:
                for line in file:
                    write_content += "0" + line[1:]
            with open(file_path, "w") as file:
                file.write(write_content)

        # generate obj.data, obj.names
        obj_names_path = os.path.join(self.target_dir, "obj.names")
        obj_data_path = os.path.join(self.target_dir, "obj.data")
        with open(obj_names_path, "w") as file:
            file.write("hands")
        with open(obj_data_path, "w") as file:
            file.write("classes = 1\n")
            file.write(f"train = {self.train_path}\n")
            file.write(f"valid = {self.test_path}\n")  # use test data for validation during the training
            file.write(f"test = {self.test_path}\n")
            file.write(f"names = {obj_names_path}\n")
            file.write(f"backup = {self.backup_dir}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_path", type=str, help="the path of train id")
    parser.add_argument("--img_dir", type=str, help="The dir of image data")
    parser.add_argument("--label_dir", type=str, help="The dir of label data")
    parser.add_argument("--target_dir", type=str, help="The dir of train/test/valid data")
    flags, _ = parser.parse_known_args(sys.argv[1:])
    preTrainData = PreTrainData(flags)
    preTrainData.load_data()
    preTrainData.prepare_darknet_data()
