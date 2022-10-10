import os
import argparse
import sys
import glob
from scripts.utils.logger import Logger
logger = Logger()
from scripts.utils.utils import YoloUtils
import numpy as np


class MetaTester(object):
    def __init__(self, flags):
        self.origin_img_dir = flags.origin_img_dir.rstrip("/")
        self.mutate_img_dir = flags.mutate_img_dir.rstrip("/")
        self.mutate_type = ""
        self.idntfr = ""
        if "object" in self.mutate_img_dir or "Object" in self.mutate_img_dir:
            self.mutate_type = "object"
        if "B" in self.mutate_img_dir:
            self.mutate_type = "background"
        if "Gaussian" in self.mutate_img_dir:
            self.mutate_type = "gaussian"
        self.origin_label_dir = flags.origin_label_dir.rstrip("/")
        self.output_dir = flags.output_dir
        self.weights_path = flags.weights_path
        self.only_train = flags.only_train
        self.origin_images = glob.glob(f"{self.origin_img_dir}/*.jpg")
        self.mutate_images = glob.glob(f"{self.mutate_img_dir}/*.jpg")
        self.origin_pred = {}
        self.mutate_pred = {}
        self.threshold = flags.threshold

    @staticmethod
    def _get_label(label_dir):
        """
        param label_dir: the dir of label files
        return labels: {file_name1: [label1, label2], file_name2: [label1, label2]}
        """
        labels = {}
        for label_path in glob.glob(f"{label_dir}/*.txt"):
            file_name = os.path.basename(label_path)[:-4]
            labels[file_name] = []
            with open(label_path, "r") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                arr = line.split(" ")
                arr = list(map(float, arr))
                arr[0] = int(arr[0])
                labels[file_name].append(arr)
        return labels

    def get_prediction(self):
        origin_img_name = os.path.basename(self.origin_img_dir)
        mutate_img_name = os.path.basename(self.mutate_img_dir)
        origin_output_dir = os.path.join(self.output_dir, origin_img_name)
        mutate_output_dir = os.path.join(self.output_dir, "repair", mutate_img_name, "ImageSet")
        if not os.path.exists(origin_output_dir):
            # predict on original image
            logger.info(f"Detection on {origin_img_name} Does Not Exist, Conducting Hand Detection")
            os.system(f"python -u -m scripts.evaluation.detect "
                      f"-i=all --img_dir={self.origin_img_dir} "
                      f"-w={self.weights_path} "
                      f"--save_dir={origin_output_dir}")
        else:
            logger.info(f"Detection on {origin_img_name} Exists, Loading the Detection")
        # origin_pred: {img_id: [label1, label2], ..., }
        self.origin_pred = self._get_label(origin_output_dir)
        if not os.path.exists(mutate_output_dir):
            # predict on mutate image
            logger.info(f"Detection on {mutate_output_dir} Does Not Exist, Conducting Hand Detection")
            os.system(f"python -u -m scripts.evaluation.detect "
                      f"-i=all --img_dir={self.mutate_img_dir} "
                      f"-w={self.weights_path} "
                      f"--save_dir={mutate_output_dir}")
        else:
            logger.info(f"Detection on {mutate_output_dir} Exists, Loading the Detection")
        # mutate_pred: {file_name: [label1, label2]}
        self.mutate_pred = self._get_label(mutate_output_dir)

    def analyze_error(self, ):
        origin_res_list = {"correct": 0, "localization": 0, "similar": 0, "other": 0, "background": 0}
        mutate_res_list = {"correct": 0, "localization": 0, "similar": 0, "other": 0, "background": 0}
        labels = self._get_label(self.origin_label_dir)

        def _analyze_error(hand_labels, pred):
            if len(hand_labels) == 0:
                return "background"
            for label in hand_labels:
                threshold = YoloUtils.overlapping(label, pred)
                if threshold < 0.1:
                    return "background"
                pred_label = pred[0]
                if 0.1 <= threshold < 0.5:
                    return "localization"
                else:
                    return "correct"

        img_id_list = []
        if self.only_train == 1:
            # We only evaluate the image that belong to the training_id.txt
            with open("./data_company/testing_id.txt") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                img_id_list.append(line)
        for i, mutate_id in enumerate(self.mutate_pred):
            if (i + 1) % 500 == 0:
                logger.info(f'Progress: {str(i + 1)}')
            img_id = mutate_id.split("-")[0]
            img_labels = labels[img_id]
            if len(img_id_list) != 0 and img_id in img_id_list:
                # We only evaluate the image that belong to the training_id.txt
                logger.info(f"Find Test Images, Exclude!")
                continue
            mutate_preds = self.mutate_pred[mutate_id]
            for j in range(len(mutate_preds)):
                error_type = _analyze_error(img_labels, mutate_preds[j])
                mutate_res_list[error_type] += 1
        for i, img_id in enumerate(self.origin_pred):
            if (i + 1) % 500 == 0:
                logger.info(f'Progress: {str(i + 1)}')
            img_labels = labels[img_id]
            if len(img_id_list) != 0 and img_id in img_id_list:
                # We only evaluate the image that belong to the training_id.txt
                logger.info(f"Find Test Images, Exclude!")
                continue
            origin_preds = self.origin_pred[img_id]
            for j in range(len(origin_preds)):
                error_type = _analyze_error(img_labels, origin_preds[j])
                origin_res_list[error_type] += 1
        return origin_res_list, mutate_res_list

    def evaluate(self, ):
        self.get_prediction()
        origin_res_list, mutate_res_list = self.analyze_error()
        print(origin_res_list)
        print(mutate_res_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-oi", "--origin_img_dir", type=str, default="./data_company/ImageSet", help="The dir of original images")
    parser.add_argument("-mi", "--mutate_img_dir", type=str, default="./data_company/MutatedSet/objects", help="The dir of mutated images")
    parser.add_argument("-ol", "--origin_label_dir", type=str, default="./data_company/Labels/", help="The dir of original labels")
    parser.add_argument("-od", "--output_dir", default="./outputs", help="The dir of yolo output")
    parser.add_argument("-w", "--weights_path", default="./data_company/working_dir/origin_model/backup/cross-hands_best.weights", type=str, help="The path of model weights")
    parser.add_argument("-t", "--threshold", type=float, default=0.3, help="Confidence threshold to detect hands")
    parser.add_argument('--only_train', type=int, default=1, help="Whether we only consider the training image")
    flags, unknown = parser.parse_known_args(sys.argv[1:])
    metaTester = MetaTester(flags)
    metaTester.evaluate()