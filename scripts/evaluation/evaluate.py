import os
import argparse
import sys
import glob
from scripts.utils.logger import Logger
logger = Logger()
from scripts.utils.utils import YoloUtils
import numpy as np


# image width and height
WIDTH = 640
HEIGHT = 48


class MetaTester(object):
    def __init__(self, flags):
        self.origin_img_dir = flags.origin_img_dir.rstrip("/")
        self.mutate_img_dir = flags.mutate_img_dir.rstrip("/")
        self.origin_label_dir = flags.origin_label_dir.rstrip("/")
        self.output_dir = flags.output_dir
        self.weights_path = flags.weights_path
        self.origin_images = glob.glob(f"{self.origin_img_dir}/*.jpg")
        self.mutate_images = glob.glob(f"{self.mutate_img_dir}/*.jpg")
        self.origin_pred = {}
        self.mutate_pred = {}
        self.threshold = flags.threshold

    @staticmethod
    def _get_label(label_dir):
        """
        param label_dir: the dir of label files
        return labels: {img_id1: [label1, label2], img_id2: [label1, label2]}
        """
        labels = {}
        for label_path in glob.glob(f"{label_dir}/*.txt"):
            img_id = os.path.basename(label_path)[:-4]
            labels[img_id] = []
            with open(label_path, "r") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                arr = line.split(" ")
                arr = list(map(float, arr))
                arr[0] = int(arr[0])
                labels[img_id].append(arr)
        return labels

    def get_prediction(self):
        origin_img_name = os.path.basename(self.origin_img_dir)
        mutate_img_name = os.path.basename(self.mutate_img_dir)
        origin_output_dir = os.path.join(self.output_dir, origin_img_name)
        mutate_output_dir = os.path.join(self.output_dir, mutate_img_name)
        if not os.path.exists(origin_output_dir):
            # predict on original image
            logger.info(f"Detection on {origin_img_name} Does Not Exist, Conducting Hand Detection")
            os.system(f"python -u -m scripts.evaluation.detect "
                      f"-i=all --img_dir={self.origin_img_dir} "
                      f"-w={self.weights_path} "
                      f"--save_dir={origin_output_dir}")
        else:
            logger.info(f"Detection on {origin_img_name} Exists, Loading the Detection")
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
        self.mutate_pred = self._get_label(mutate_output_dir)
        def rename_img_id(pred):
            # we need to remove the "O" or "B" in the mutate filename
            return {k[:-1]: v for k, v in pred.items()}
        self.mutate_pred = rename_img_id(self.mutate_pred)

    def compare_prediction(self, ):
        res_id_list = {"11": [], "10": [], "01": [], "00": []}
        labels = self._get_label(self.origin_label_dir)

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

        for i, img in enumerate(labels):
            if (i + 1) % 500 == 0:
                logger.info(f'Progress: {str(i + 1)}')
            img_labels = labels[img]  # obtain the hand labels for each image
            origin_preds = self.origin_pred[img]
            for j in range(len(img_labels)):
                # iterate hands, each hand will have a mutate image and its prediction result
                hand_id = f"{img}-{str(j)}"
                mutate_preds = self.mutate_pred[hand_id]
                origin_detection = _is_detected(img_labels[j], origin_preds)
                mutate_detection = _is_detected(img_labels[j], mutate_preds)
                res_id_list[f"{int(origin_detection)}{int(mutate_detection)}"].append(hand_id)
        logger.info("Finish Comparing Detection Result, Saving The Result")
        np.save(f"res_{os.path.basename(self.origin_img_dir)}_{os.path.basename(self.mutate_img_dir)}.npy", res_id_list)
        logger.info(f"11: {len(res_id_list['11'])}, 10: {len(res_id_list['10'])}, "
                    f"01: {len(res_id_list['01'])}, 00: {len(res_id_list['00'])}")
        return res_id_list

    def save_violate(self, res_id_list):
        mutate_base = os.path.basename(self.mutate_img_dir)
        identifier = ""
        if "object" in self.mutate_img_dir:
            violate_list = ["11", "01"]
            identifier = "O"
        violate_img_id = []
        for vio in violate_list:
            violate_img_id += res_id_list[vio]
        with open(f"{mutate_base}_violations.txt", "w") as file:
            text = ""
            for img_id in violate_img_id:
                text += img_id + identifier + "\n"
            file.write(text)

    def evaluate(self, ):
        self.get_prediction()
        res_id_list = self.compare_prediction()
        self.save_violate(res_id_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-oi", "--origin_img_dir", type=str, default="./data/ImageSet", help="The dir of original images")
    parser.add_argument("-mi", "--mutate_img_dir", type=str, default="./data/MutatedSet/objects", help="The dir of mutated images")
    parser.add_argument("-ol", "--origin_label_dir", type=str, default="./data/Labels/", help="The dir of original labels")
    parser.add_argument("-od", "--output_dir", default="./outputs", help="The dir of yolo output")
    parser.add_argument("-w", "--weights_path", default="./data/working_dir/origin_model/backup/cross-hands_best.weights", type=str, help="The path of model weights")
    parser.add_argument("-t", "--threshold", type=float, default=0.3, help="Confidence threshold to detect hands")
    flags, unknown = parser.parse_known_args(sys.argv[1:])
    metaTester = MetaTester(flags)
    metaTester.evaluate()
