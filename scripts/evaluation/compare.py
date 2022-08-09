import os
import argparse
import sys
import glob
from scripts.utils.logger import Logger
logger = Logger()
from scripts.utils.utils import YoloUtils
import numpy as np


class MetaComparator(object):
    def __init__(self, flags):
        self.origin_weights_path = flags.origin_weights_path
        self.repair_weights_path = flags.repair_weights_path
        self.label_dir = flags.label_dir.rstrip("/")
        self.images_dir = flags.images_dir.rstrip("/")
        self.output_dir = flags.output_dir.rstrip("/")
        self.origin_output_dir = flags.origin_output_dir.rstrip("/")
        self.threshold = flags.threshold
        self.only_train = flags.only_train
        self.mutate_type = ""
        self.idntfr = ""
        self.images = glob.glob(f"{self.images_dir}/*.jpg")
        self.origin_pred = {}
        self.repair_pred = {}

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
        img_name = os.path.basename(self.images_dir)
        origin_output_dir = os.path.join(self.origin_output_dir, img_name)
        repair_output_dir = os.path.join(self.output_dir, img_name)
        if not os.path.exists(origin_output_dir):
            # predict on original image
            logger.info(f"Detection on {origin_output_dir} Does Not Exist, Conducting Hand Detection")
            os.system(f"python -u -m scripts.evaluation.detect "
                      f"-i=all --img_dir={self.images_dir} "
                      f"-w={self.origin_weights_path} "
                      f"--save_dir={origin_output_dir}")
        else:
            logger.info(f"Detection on {origin_output_dir} Exists, Loading the Detection")
        # origin_pred: {img_id: [label1, label2], ..., }
        self.origin_pred = self._get_label(origin_output_dir)
        if not os.path.exists(repair_output_dir):
            # predict on mutate image
            logger.info(f"Detection on {repair_output_dir} Does Not Exist, Conducting Hand Detection")
            os.system(f"python -u -m scripts.evaluation.detect "
                      f"-i=all --img_dir={self.images_dir} "
                      f"-w={self.repair_weights_path} "
                      f"--save_dir={repair_output_dir}")
        else:
            logger.info(f"Detection on {repair_output_dir} Exists, Loading the Detection")
        self.repair_pred = self._get_label(repair_output_dir)

        assert len(self.repair_pred) == len(self.origin_pred)

    def compare_prediction(self, ):
        res_id_list = {"11": [], "10": [], "01": [], "00": []}
        # labels: {img_id1: [label1, label2], img_id2: [label1, label2]}
        labels = self._get_label(self.label_dir)

        def _is_detected(hand_label, preds):
            status = False
            if len(preds) == 0:
                return status
            for pred in preds:
                # Go through all prediction and check whether the hand is detected
                threshold = YoloUtils.overlapping(hand_label, pred)
                if threshold > self.threshold:
                    status = True
            return status

        img_id_list = []
        if self.only_train == 1:
            # We only evaluate the image that belong to the training_id.txt
            with open("./data_company/testing_id.txt") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                img_id_list.append(line)
        for i, img_id in enumerate(self.repair_pred):
            if (i + 1) % 500 == 0:
                logger.info(f'Progress: {str(i + 1)}')
            img_labels = labels[img_id]
            origin_preds = self.origin_pred[img_id]
            repair_preds = self.repair_pred[img_id]
            if len(img_id_list) != 0 and img_id in img_id_list:
                # We only evaluate the image that belong to the training_id.txt
                logger.info(f"Find Test Images, Exclude!")
                continue
            for hand_id in range(len(img_labels)):
                origin_detection = _is_detected(img_labels[hand_id], origin_preds)
                mutate_detection = _is_detected(img_labels[hand_id], repair_preds)
                res_id_list[f"{int(origin_detection)}{int(mutate_detection)}"].append(f"{img_id}-{hand_id}")
        logger.info("Finish Comparing Detection Result")
        logger.info(f"11: {len(res_id_list['11'])}, 10: {len(res_id_list['10'])}, "
                    f"01: {len(res_id_list['01'])}, 00: {len(res_id_list['00'])}")
        return res_id_list

    def save_violate(self, res_id_list):
        target_list = ["01"]
        target_id_list = []
        for target_id in target_list:
            target_id_list += res_id_list[target_id]
        with open(f"target.txt", "w") as file:
            text = ""
            for target_id in target_id_list:
                text += target_id + "\n"
            file.write(text)
        import shutil
        target_dir = os.path.join(self.output_dir, "target")
        os.system(f"rm -rf {target_dir}")
        os.makedirs(target_dir)
        for target_id in target_id_list:
            img_name = os.path.basename(self.images_dir)
            img_id = target_id.split("-")[0]
            target_img_dir = os.path.join(target_dir, img_id)
            if not os.path.exists(target_img_dir):
                os.makedirs(target_img_dir)
            else:
                continue
            origin_image_dir = os.path.join(self.origin_output_dir, img_name)
            repair_image_dir = os.path.join(self.output_dir, img_name)
            origin_list = glob.glob(f"{origin_image_dir}/{img_id}*")
            repair_list = glob.glob(f"{repair_image_dir}/{img_id}*")
            for file_path in origin_list:
                shutil.copy(file_path, target_img_dir)
            for file_path in repair_list:
                file_name = os.path.basename(file_path)
                new_file_name = file_name.replace(".txt", "-repair.txt")
                new_file_name = new_file_name.replace(".jpg", "-repair.jpg")
                shutil.copy(file_path, os.path.join(target_img_dir, new_file_name))

    def evaluate(self, ):
        self.get_prediction()
        res_id_list = self.compare_prediction()
        self.save_violate(res_id_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ow", "--origin_weights_path", type=str, default="./data_company/working_dir/origin_model/backup/cross-hands_best.weights", help="The dir of original weights")
    parser.add_argument("-rw", "--repair_weights_path", type=str, default="./data_company/MutatedSet/objects", help="The dir of mutated images")
    parser.add_argument("-l", "--label_dir", type=str, default="./data_company/Labels/", help="The dir of labels")
    parser.add_argument("-i", "--images_dir", type=str, default="./data_company/ImageSet", help="The dir of images")
    parser.add_argument("-od", "--output_dir", default="./outputs/company/repair/B_guassian_160_fixMutRatio_centerXY_01", help="The dir of yolo output")
    parser.add_argument("-ood", "--origin_output_dir", default="./outputs/company")
    parser.add_argument("-t", "--threshold", type=float, default=0.3, help="Confidence threshold to detect hands")
    parser.add_argument('--only_train', type=int, default=0, help="Whether we only consider the training image")
    flags, unknown = parser.parse_known_args(sys.argv[1:])
    metaComparator = MetaComparator(flags)
    metaComparator.evaluate()

