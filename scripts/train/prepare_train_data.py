import os
from sklearn.model_selection import train_test_split
from scripts.utils.logger import Logger
from scripts.utils.utils import get_files, deprecated
import glob
import shutil
import argparse
import sys
logger = Logger()
MAPPING_DICT = {"popsquare": "./data_company", "coco": "./data_coco"}


class PreTrainData(object):
    def __init__(self, flags):
        self.data_path = flags.source_path
        self.dataset = flags.dataset
        self.data_root_dir = MAPPING_DICT[self.dataset].rstrip("/")
        self.img_list = []
        self.target_dir = flags.target_dir.rstrip("/")
        self.img_dir = flags.img_dir.rstrip("/")
        self.label_dir = flags.label_dir.rstrip("/")
        self.obj_dir = os.path.join(self.target_dir, "obj").rstrip("/")
        self.backup_dir = os.path.join(self.target_dir, "backup").rstrip("/")
        self.train_path = os.path.join(self.target_dir, "train.txt")
        self.valid_path = os.path.join(self.target_dir, "valid.txt")
        self.test_path = os.path.join(self.target_dir, "test.txt")
        self.append = flags.append  # 0: do not append (default), 1: append without removing original data
        self.initiate_dirs()

    @deprecated
    def _prepare_img_label(self, id: str):
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

    def initiate_dirs(self):
        if os.path.exists(self.target_dir) and self.append == 0:
            shutil.rmtree(self.target_dir, ignore_errors=True)
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
        if self.data_path != f"{self.data_root_dir}/training_id.txt" and self.append == 0:
            # if append is 0, we assume the original training image has not been added to the working dir.
            # Therefore we do it.
            with open(f"{self.data_root_dir}/training_id.txt", "r") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                self.img_list.append(line)

    def _split_train_valid_test(self, test_ratio=0.2):
        if test_ratio == 0:
            return self.img_list, []
        else:
            train_list, valid_list = train_test_split(self.img_list, test_size=0.2)
            return train_list, valid_list

    def prepare_label(self):
        logger.info("Preparing Labels")
        os.system(f"find {self.data_root_dir}/Labels/ -name '*.txt' -exec cp " + "{}" + f" {self.obj_dir} \\;")
        if self.label_dir == "empty":
            img_list = os.listdir(self.img_dir)
            for img in img_list:
                img_name = img[:-4]
                label_path = os.path.join(self.obj_dir, f"{img_name}.txt")
                os.system(f"touch {label_path}")
        elif self.label_dir == "same":
            img_list = os.listdir(self.img_dir)
            for img in img_list:
                mutate_id = img[:-4]
                img_id = mutate_id.split("-")[0]
                label_path = os.path.join(self.obj_dir, f"{mutate_id}.txt")
                shutil.copy(f"{self.data_root_dir}/Labels/{img_id}.txt", f"{label_path}")
        elif self.label_dir != f"{self.data_root_dir}/Labels":
            os.system(f"find {self.label_dir} -name '*.txt' -exec cp " + "{}" + f" {self.obj_dir} \\;")

    def prepare_img(self):
        logger.info("Preparing Images")
        os.system(f"find {self.img_dir} -name '*.jpg' -exec cp " + "{}" + f" {self.obj_dir} \\;")
        if self.append == 0 and self.img_dir != f"{self.data_root_dir}/ImageSet":
            # if we append the target directory, we assume that original training data have been added
            os.system(f"find {self.data_root_dir}/ImageSet/ -name '*.jpg' -exec cp " + "{}" + f" {self.obj_dir} \\;")

    def prepare_train_valid_test(self):
        train_list, valid_list = self._split_train_valid_test(test_ratio=0.0)
        test_list = []
        with open(f"{self.data_root_dir}/testing_id.txt", "r") as file:
            content = file.read().split("\n")[:-1]
            for line in content:
                test_list.append(line)
        with open(self.train_path, "a") as file:
            for train_id in train_list:
                target_file_path = os.path.join(self.obj_dir, f"{train_id}.jpg")
                file.write(target_file_path+"\n")
        with open(self.valid_path, "a") as file:
            for valid_id in valid_list:
                target_file_path = os.path.join(self.obj_dir, f"{valid_id}.jpg")
                file.write(target_file_path+"\n")
        with open(self.test_path, "w") as file:
            for test_id in test_list:
                target_file_path = os.path.join(self.obj_dir, f"{test_id}.jpg")
                file.write(target_file_path+"\n")
        with open(self.train_path, "r") as file:
            content = file.read().split("\n")[:-1]
        train_list = []
        for line in content:
            train_list.append(line)
        logger.info(f"Total Number of Training Set: {len(train_list)}")
        logger.info(f"Total Number of Validation Set: {len(valid_list)}")
        logger.info(f"Total Number of Test Set: {len(test_list)}")

    def prepare_obj(self):
        # TODO: Need To Change This Logic Before Evaluating On COCO DataSet
        if self.dataset == "popsquare":
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
        if self.dataset == "popsquare":
            with open(obj_names_path, "w") as file:
                file.write("hands")
        elif self.dataset == "coco":
            shutil.copy("./cfg/coco.names", obj_names_path)
        else:
            raise ValueError("Undefined Dataset !!!")
        with open(obj_data_path, "w") as file:
            file.write("classes = 1\n")
            file.write(f"train = {self.train_path}\n")
            file.write(f"valid = {self.test_path}\n")  # use test data for validation during the training
            file.write(f"test = {self.test_path}\n")
            file.write(f"names = {obj_names_path}\n")
            file.write(f"backup = {self.backup_dir}\n")

    def prepare_darknet_data(self):
        self.prepare_img()
        self.prepare_label()
        self.prepare_train_valid_test()
        self.prepare_obj()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_path", type=str, help="the path of train id")
    parser.add_argument("--img_dir", type=str, help="The dir of image data")
    parser.add_argument("--label_dir", type=str, help="The dir of label data")
    parser.add_argument("--target_dir", type=str, help="The dir of train/test/valid data")
    parser.add_argument("--append", type=int, default=0, help="Whether to add images to existing work dir")
    parser.add_argument("--dataset", type=str, default="popsquare", help="The type of the dataset")
    flags, _ = parser.parse_known_args(sys.argv[1:])
    preTrainData = PreTrainData(flags)
    preTrainData.load_data()
    preTrainData.prepare_darknet_data()
