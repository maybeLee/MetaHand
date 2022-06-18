import os
import argparse
import sys
import glob
from scripts.utils.logger import Logger
logger = Logger()
from scripts.utils.utils import YoloUtils
import numpy as np
from scripts.train.prepare_train_data import MAPPING_DICT


class MetaTester(object):
    def __init__(self, flags):
        self.origin_img_dir = flags.origin_img_dir.rstrip("/")
        self.mutate_img_dir = flags.mutate_img_dir.rstrip("/")
        self.mutate_type = ""
        self.idntfr = ""
        if "object" in self.mutate_img_dir or "Object" in self.mutate_img_dir:
            # object: only preserve the object
            self.mutate_type = "object"
        if "B" in self.mutate_img_dir:
            # B: only preserver the background, mutation operator such as CenterEraseMutation
            self.mutate_type = "background"
        if "Gaussian" in self.mutate_img_dir:
            # Add gaussian noise to the object or background, label will be preserved
            self.mutate_type = "gaussian"
        self.origin_label_dir = flags.origin_label_dir.rstrip("/")
        self.output_dir = flags.output_dir
        self.weights_path = flags.weights_path
        self.only_train = flags.only_train
        self.dataset = flags.dataset
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
                new_arr = []
                for i in arr:
                    try:
                        new_arr.append(float(i))
                    except:
                        pass
                arr = new_arr
                arr[0] = int(arr[0])
                labels[file_name].append(arr)
        return labels

    def get_prediction(self):
        origin_img_name = os.path.basename(self.origin_img_dir)
        mutate_img_name = os.path.basename(self.mutate_img_dir)
        origin_output_dir = os.path.join(self.output_dir, origin_img_name)
        mutate_output_dir = os.path.join(self.output_dir, mutate_img_name)
        if self.dataset == "popsquare":
            cfg_path = "./cfg/cross-hands.cfg"
        elif self.dataset == "voc":
            cfg_path = "./cfg/yolov3-voc.cfg"
        elif self.dataset == "coco":
            cfg_path = "./cfg/yolov3.cfg"
        else:
            raise ValueError("Undefined Dataset Found!!")
        if not os.path.exists(origin_output_dir):
            # predict on original image
            logger.info(f"Detection on {origin_img_name} Does Not Exist, Conducting Hand Detection")
            os.system(f"python -u -m scripts.evaluation.detect "
                      f"-i=all --img_dir={self.origin_img_dir} "
                      f"-w={self.weights_path} "
                      f"--save_dir={origin_output_dir} "
                      f"--cfg={cfg_path} "
                      f"--dataset={self.dataset}"
                      )
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
                      f"--save_dir={mutate_output_dir} "
                      f"--cfg={cfg_path} "
                      f"--dataset={self.dataset}"
                      )
        else:
            logger.info(f"Detection on {mutate_output_dir} Exists, Loading the Detection")
        # mutate_pred: {file_name: [label1, label2]}
        self.mutate_pred = self._get_label(mutate_output_dir)

    def compare_prediction(self, ):
        res_id_list = {"11": [], "10": [], "01": [], "00": []}
        # labels: {img_id1: [label1, label2], img_id2: [label1, label2]}
        labels = self._get_label(self.origin_label_dir)

        def _is_detected(hand_label, preds):
            status = False
            if len(preds) == 0:
                return status
            for pred in preds:
                # Go through all prediction and check whether the hand is detected
                # We only check the IoU if the predicted category is the same as the ground truth
                pred_label = pred[0]
                if pred_label != hand_label[0]:
                    continue
                threshold = YoloUtils.overlapping(hand_label, pred)
                if threshold > self.threshold:
                    status = True
            return status

        img_id_list = []
        if self.only_train == 1:
            # We only evaluate the image that belong to the training_id.txt
            # No need for this under coco scenario because we did not involve test images when mutating
            with open(f"{MAPPING_DICT[self.dataset]}/testing_id.txt") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                if self.dataset == "voc":
                    # if the dataset is voc, the testing_id stores the path of file
                    # example: /root/data_voc/images/val2014/2008_008439.jpg
                    img_id = line.split("2014/")[-1].split(".jpg")[0]
                else:
                    # if the dataset is popsquare, the testing_id only stores the id of file
                    img_id = line
                img_id_list.append(img_id)
        for i, mutate_id in enumerate(self.mutate_pred):
            if (i + 1) % 500 == 0:
                logger.info(f'Progress: {str(i + 1)}')
            img_id = mutate_id.split("-")[0]
            if len(img_id_list) != 0 and img_id in img_id_list:
                # We only evaluate the image that belong to the training_id.txt
                logger.info(f"Find Test Images, Exclude!")
                continue
            img_labels = labels[img_id]
            origin_preds = self.origin_pred[img_id]
            mutate_preds = self.mutate_pred[mutate_id]
            if self.mutate_type == "object":
                hand_id = int(mutate_id.split("-")[1].rstrip("O"))
                origin_detection = _is_detected(img_labels[hand_id], origin_preds)
                mutate_detection = _is_detected(img_labels[hand_id], mutate_preds)
                res_id_list[f"{int(origin_detection)}{int(mutate_detection)}"].append(mutate_id)
            elif self.mutate_type == "background" or self.mutate_type == "gaussian":
                for j in range(len(img_labels)):
                    origin_detection = _is_detected(img_labels[j], origin_preds)
                    mutate_detection = _is_detected(img_labels[j], mutate_preds)
                    res_id_list[f"{int(origin_detection)}{int(mutate_detection)}"].append(mutate_id)
            else:
                raise ValueError("Unsupported Mutation Type!")
        logger.info("Finish Comparing Detection Result. Start Filtering The Duplicated Images")
        for type in res_id_list:
            # We filter out duplicated images
            img_list = []
            for img_path in res_id_list[type]:
                if img_path not in img_list:
                    img_list.append(img_path)
                else:
                    continue
            res_id_list[type] = img_list
        logger.info("Finish Filtering the Duplicated Images. Saving The Result")
        if not os.path.exists("./results"):
            os.makedirs("./results")
        np.save(f"./results/res_{os.path.basename(self.origin_img_dir)}_{os.path.basename(self.mutate_img_dir)}.npy", res_id_list)
        logger.info(f"11: {len(res_id_list['11'])}, 10: {len(res_id_list['10'])}, "
                    f"01: {len(res_id_list['01'])}, 00: {len(res_id_list['00'])}")
        return res_id_list

    def save_violate(self, res_id_list):
        mutate_base = os.path.basename(self.mutate_img_dir)
        if self.mutate_type == "object":
            violate_list = ["10", "01"]
        elif self.mutate_type == "background":
            violate_list = ["01", "11"]
        elif self.mutate_type == "gaussian":
            violate_list = ["01", "10"]
        else:
            raise ValueError("Unsupported Mutation Type!")
        violate_mutate_id_list = []
        for vio in violate_list:
            violate_mutate_id_list += res_id_list[vio]
        with open(f"{mutate_base}_violations.txt", "w") as file:
            text = ""
            for violate_mutate_id in violate_mutate_id_list:
                violate_mutate_path = os.path.join(self.mutate_img_dir, f"{violate_mutate_id}.jpg")
                text += violate_mutate_path + "\n"
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
    parser.add_argument('--only_train', type=int, default=1, help="Whether we only consider the training image")
    parser.add_argument("--dataset", type=str, default="popsquare", help="The type of the dataset")
    flags, unknown = parser.parse_known_args(sys.argv[1:])
    metaTester = MetaTester(flags)
    metaTester.evaluate()
