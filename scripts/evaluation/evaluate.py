import os
import argparse
import sys
import glob
from scripts.utils.logger import Logger
logger = Logger()
from scripts.utils.utils import YoloUtils
import numpy as np
from scripts.train.prepare_train_data import MAPPING_DICT


def xyxy2xywh(x):
    # Convert nx4 boxes from [x1, y1, x2, y2] to [x, y, w, h] where xy1=top-left, xy2=bottom-right
    y = np.copy(x)
    y[:, 0] = (x[:, 0] + x[:, 2]) / 2  # x center
    y[:, 1] = (x[:, 1] + x[:, 3]) / 2  # y center
    y[:, 2] = x[:, 2] - x[:, 0]  # width
    y[:, 3] = x[:, 3] - x[:, 1]  # height
    return y


def segments2boxes(segments):
    # Convert segment labels to box labels, i.e. (cls, xy1, xy2, ...) to (cls, xywh)
    boxes = []
    for s in segments:
        x, y = s.T  # segment xy
        boxes.append([x.min(), y.min(), x.max(), y.max()])  # cls, xyxy
    return xyxy2xywh(np.array(boxes))  # cls, xywh


class MetaTester(object):
    """MetaTester for evaluating a trained model on mutated images
    """

    def __init__(self, flags):
        """
        Initiating the `MetaTester` class.
        :param flags: flags containing all necessary variables.
        flags.origin_img_dir: the directory of original images
        flags.mutate_img_dir: the directory of mutated images
        flags.origin_label_dir: the directory of original images' labels
        flags.weights_path: the path stores the weights of the trained model
        flags.only_train: for popsquare only, flags for considering training images
        flags.output_dir: the directory storing model's prediction result on each image
        flags.mr: 1: MR-1 (corrupting object-relevant features), 2: MR-2 (corrupting object-irrelevant features)
        flags.dataset: the type of dataset (e.g., coco, popsquare, egohands, imagenet)
        flags.threshold: threshold used to determine the mis-detection
        flags.jogs: number of parallel jobs
        """

        self.origin_img_dir = flags.origin_img_dir.rstrip("/")
        self.mutate_img_dir = flags.mutate_img_dir.rstrip("/")
        self.mr = flags.mr
        self.idntfr = ""
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
        self.jobs = flags.jobs

    @staticmethod
    def _get_label(label_dir, segments=False):
        """
        :param label_dir: The dir of label files
        :param segments: Whether the label is stored in the segments format, if so, we need to convert it to xywh
        :return: {file_name1: [label1, label2], file_name2: [label1, label2]}
        Note that the file_name does not keep the extension
        """
        labels = {}
        for label_path in glob.glob(f"{label_dir}/*.txt"):
            file_name = os.path.basename(label_path)[:-4]
            labels[file_name] = []
            if segments is True:
                with open(label_path, 'r') as file:
                    l = [x.split() for x in file.read().strip().splitlines()]
                    if any([len(x) > 8 for x in l]):  # is segment
                        classes = np.array([x[0] for x in l], dtype=np.float32)
                        segments = [np.array(x[1:], dtype=np.float32).reshape(-1, 2) for x in l]  # (cls, xy1...)
                        l = np.concatenate((classes.reshape(-1, 1), segments2boxes(segments)), 1)  # (cls, xywh)
                    l = np.array(l, dtype=np.float32)
                if len(l):
                    assert l.shape[1] == 5, 'labels require 5 columns each'
                    assert (l >= 0).all(), 'negative labels'
                    assert (l[:, 1:] <= 1).all(), 'non-normalized or out of bounds coordinate labels'
                    assert np.unique(l, axis=0).shape[0] == l.shape[0], 'duplicate labels'
                labels[file_name] = l.tolist()
            else:
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
        """
        Get the prediction of trained model on both original images and mutated images
        :return: None
        """
        origin_img_name = os.path.basename(self.origin_img_dir)
        mutate_img_name = os.path.basename(self.mutate_img_dir)
        origin_output_dir = os.path.join(self.output_dir, origin_img_name)
        mutate_output_dir = os.path.join(self.output_dir, mutate_img_name)
        if self.dataset == "yolov7":
            origin_output_dir = os.path.join(origin_output_dir, "labels")
            mutate_output_dir = os.path.join(origin_output_dir, "labels")

        if self.dataset == "popsquare":
            cfg_path = "./cfg/cross-hands.cfg"
        elif self.dataset == "voc":
            cfg_path = "./cfg/yolov3-voc.cfg"
        elif self.dataset == "coco":
            cfg_path = "./cfg/yolov3.cfg"
        elif self.dataset == "egohands":
            cfg_path = "./cfg/egohands.cfg"
        elif self.dataset == "imagenet":
            cfg_path = "./cfg/yolov3-imagenet.cfg"
        else:
            raise ValueError("Undefined Dataset Found!!")
        if not os.path.exists(origin_output_dir):
            # predict on original image
            logger.info(f"Detection on {origin_img_name} Does Not Exist, Conducting Object Detection")
            if self.dataset == "yolov7":
                os.system(f"python -u -m scripts.evaluation.detect_parallel_yolov7 "
                          f"--img_dir={self.origin_img_dir} "
                          f"-w={self.weights_path} "
                          f"-j={self.jobs} "
                          )
            else:
                os.system(f"python -u -m scripts.evaluation.detect "
                          f"-i=all --img_dir={self.origin_img_dir} "
                          f"-w={self.weights_path} "
                          f"-j={self.jobs} "
                          f"--save_dir={origin_output_dir} "
                          f"--cfg={cfg_path} "
                          f"--dataset={self.dataset}"
                          )
        else:
            logger.info(f"Detection on {origin_img_name} Exists, Loading the Detection")
        # origin_pred: {file_name: [label1, label2], ..., }
        self.origin_pred = self._get_label(origin_output_dir)
        if not os.path.exists(mutate_output_dir):
            # predict on mutate image
            logger.info(f"Detection on {mutate_output_dir} Does Not Exist, Conducting Object Detection")
            if self.dataset == "yolov7":
                os.system(f"python -u -m scripts.evaluation.detect_parallel_yolov7 "
                          f"--img_dir={self.mutate_img_dir} "
                          f"-w={self.weights_path} "
                          f"-j={self.jobs} "
                          )
            else:
                os.system(f"python -u -m scripts.evaluation.detect "
                          f"-i=all --img_dir={self.mutate_img_dir} "
                          f"-w={self.weights_path} "
                          f"-j={self.jobs} "
                          f"--save_dir={mutate_output_dir} "
                          f"--cfg={cfg_path} "
                          f"--dataset={self.dataset}"
                          )
        else:
            logger.info(f"Detection on {mutate_output_dir} Exists, Loading the Detection")
        # mutate_pred: {file_name: [label1, label2]}
        self.mutate_pred = self._get_label(mutate_output_dir)

    def _is_detected(self, label, preds):
        """
        Check if the preds correctly detect the hand
        :param label: [class_id, x, y, width, height]
        :param preds: [[class_id, x, y, width, height], [...], ...]
        :return: bool, True: preds can detect the label, False: preds cannot detect the label
        """
        status = False
        if len(preds) == 0:
            return status
        for pred in preds:
            # Go through all prediction and check whether the hand is detected
            # We only check the IoU if the predicted category is the same as the ground truth
            pred_label = pred[0]
            if pred_label != label[0]:
                continue
            threshold = YoloUtils.overlapping(label, pred)
            if threshold > self.threshold:
                status = True
        return status

    def compare_prediction(self, ):
        res_id_list = {"11": [], "10": [], "01": [], "00": []}
        # labels: {img_id1: [label1, label2], img_id2: [label1, label2]}
        labels = self._get_label(self.origin_label_dir, self.dataset == "yolov7")
        img_id_list = []
        if self.only_train == 1 and self.dataset != "yolov7":
            # We only evaluate the image that belong to the training_id.txt
            # No need for this under coco, imagenet or egohands scenario because we did not involve test images when mutating
            with open(f"{MAPPING_DICT[self.dataset]}/testing_id.txt") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                # if the dataset is popsquare, the testing_id only stores the id of file
                img_id_list.append(line)
        # Go through each mutant, find its related original image, and the ground truth label.
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
            for j in range(len(img_labels)):
                origin_detection = self._is_detected(img_labels[j], origin_preds)
                mutate_detection = self._is_detected(img_labels[j], mutate_preds)
                res_id_list[f"{int(origin_detection)}{int(mutate_detection)}"].append(mutate_id)
        if not os.path.exists("./results"):
            os.makedirs("./results")
        np.save(f"./results/res_{os.path.basename(self.origin_img_dir)}_{os.path.basename(self.mutate_img_dir)}.npy", res_id_list)
        logger.info(f"11: {len(res_id_list['11'])}, 10: {len(res_id_list['10'])}, "
                    f"01: {len(res_id_list['01'])}, 00: {len(res_id_list['00'])}")
        return res_id_list

    def save_violate(self, res_id_list):
        mutate_base = os.path.basename(self.mutate_img_dir)
        if self.mr == 1:
            # MR-1: An image mutated by corrupting the features of target object(s) should lead to a different object
            # detection result.
            violate_list = ["11", "00"]
        elif self.mr == 2:
            # MR-2: An image mutated by not corrupting the features of target object(s) should lead to the same object
            # detection result
            violate_list = ["01", "10"]
        else:
            raise ValueError("Unsupported Mutation Type!")
        violate_mutate_id_list = []
        for vio in violate_list:
            violate_mutate_id_list += res_id_list[vio]
        logger.info("Finish Comparing Detection Result. Start Filtering The Duplicated Images")
        # We filter out duplicated images
        img_list = []
        for file_name in violate_mutate_id_list:
            if file_name not in img_list:
                img_list.append(file_name)
            else:
                continue
        violate_mutate_id_list = img_list
        logger.info("Finish Filtering the Duplicated Images. Saving The Result")
        with open(f"{mutate_base}_violations.txt", "w") as file:
            text = ""
            for violate_mutate_id in violate_mutate_id_list:
                if self.dataset == "popsquare":
                    # if dataset is popsquare, img_list only stores the img_name instead of the actual path
                    text += violate_mutate_id + "\n"
                else:
                    violate_mutate_path = os.path.join(self.mutate_img_dir, f"{violate_mutate_id}.jpg")
                    text += violate_mutate_path + "\n"
            file.write(text)

    def evaluate(self, ):
        self.get_prediction()
        res_id_list = self.compare_prediction()
        self.save_violate(res_id_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-oi", "--origin_img_dir", type=str, default="./data_company/ImageSet", help="The dir of original images")
    parser.add_argument("-mi", "--mutate_img_dir", type=str, default="./data_company/MutatedSet/objects", help="The dir of mutated images")
    parser.add_argument("-ol", "--origin_label_dir", type=str, default="./data_company/Labels/", help="The dir of original labels")
    parser.add_argument("-od", "--output_dir", default="./outputs", help="The dir of yolo output")
    parser.add_argument('-j', '--jobs', default=1, help='Number of parallel jobs')
    parser.add_argument("-w", "--weights_path", default="./data_company/working_dir/origin_model/backup/cross-hands_best.weights", type=str, help="The path of model weights")
    parser.add_argument("-t", "--threshold", type=float, default=0.3, help="Confidence threshold to detect hands")
    parser.add_argument('--only_train', type=int, default=1, help="Whether we only consider the training image")
    parser.add_argument("--dataset", type=str, default="popsquare", help="The type of the dataset")
    parser.add_argument("--mr", type=int, default=2, help="MR used. 1: MR-1, 2: MR-2")
    flags, unknown = parser.parse_known_args(sys.argv[1:])
    metaTester = MetaTester(flags)
    metaTester.evaluate()
