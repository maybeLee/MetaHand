import argparse
import glob
import os
import cv2
from scripts.evaluation.yolo import YOLO
from scripts.utils.logger import Logger
from scripts.train.prepare_train_data import MAPPING_DICT
from multiprocessing import Pool


logger = Logger()


def model_predict(args):
    """
    This function will load the `model` to predict images whose paths are stored in `images`.
    The detection result for each image is stored in save_dir.
    :param args: with the following arguments
    param model: model to be loaded.
    param images: paths of images to be predicted.
    param save_dir: directory to save the prediction result
    :return: total confidence and total number of detection
    """
    model, images, save_dir = args
    conf_sum = 0
    detection_count = 0
    for i, image in enumerate(images):
        logger.info(f"Progress: {i}/{len(images)}")
        mat = cv2.imread(image)
        width, height, inference_time, results = model.inference(mat)
        res_path = os.path.join(save_dir, f"{os.path.basename(image)[:-4]}.txt")
        label_path = os.path.join(save_dir, f"{os.path.basename(image)[:-4]}_label.jpg")
        with open(res_path, "a") as file:
            for res in results:
                id, name, confidence, x, y, w, h = res
                file.write("%s %s %s %s %s %s\n" % (
                    id, str(x / width), str(y / height), str(w / width), str(h / height), str(confidence)))

                cx = x + (w / 2)
                cy = y + (h / 2)

                conf_sum += confidence
                detection_count += 1

                # draw a bounding box rectangle and label on the image
                color = (255, 0, 255)
                cv2.rectangle(mat, (x, y), (x + w, y + h), color, 1)
                text = "%s (%s)" % (name, round(confidence, 2))
                cv2.putText(mat, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.25, color, 1)
            cv2.imwrite(label_path, mat)
    return conf_sum, detection_count


class Detector(object):
    def __init__(self, flags):
        self.yolo = None
        self.yolo_cfg = flags.cfg_path
        self.yolo_size = flags.size
        self.dataset = flags.dataset
        self.data_root_dir = MAPPING_DICT[self.dataset].rstrip("/")
        self.yolo_confidence = flags.confidence
        self.source_path = flags.source_path
        self.jobs = flags.jobs
        self.img_dir = flags.img_dir.rstrip("/")
        self.save_dir = flags.save_dir.rstrip("/")
        self.weights_path = flags.weights_path
        self.images = []
        self.only_train = flags.only_train
        self.initiate_dirs()

    def initiate_dirs(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def load_weights(self, ):
        if self.dataset == "popsquare" or self.dataset == "egohands":
            self.yolo = YOLO(self.yolo_cfg, self.weights_path, ["hand"])
        elif self.dataset == "coco":
            name_path = "./cfg/coco.names"
            with open(name_path, "r") as file:
                content = file.read().split("\n")[:-1]
            label_list = []
            for label in content:
                label_list.append(label)
            self.yolo = YOLO(self.yolo_cfg, self.weights_path, label_list)
        elif self.dataset == "voc":
            name_path = "./cfg/voc.names"
            with open(name_path, "r") as file:
                content = file.read().split("\n")[:-1]
            label_list = []
            for label in content:
                label_list.append(label)
            self.yolo = YOLO(self.yolo_cfg, self.weights_path, label_list)
        self.yolo.size = int(self.yolo_size)
        self.yolo.confidence = float(self.yolo_confidence)

    def load_data(self, ):
        """
        Load images stored in `self.img_dir` to detect, the image paths will be stored in list, e.g., [path1, path2, ...]
        This function has several modes, which is determined by `self.source_path`:
            if self.source_path is "all": load all images stored in `self.img_dir`
            if self.source_path is a txt file, load all images listed in the txt file from the `self.img_dir`
        :return: None
        """
        logger.info("Loading Images...")
        if self.source_path == "all":
            if self.img_dir.endswith(".jpg"):
                self.images = [self.img_dir]
            else:
                # we add all images in img_dir
                self.images = glob.glob(f"{self.img_dir}/*.jpg")
        else:
            with open(self.source_path, "r") as file:
                image_list = file.read().split("\n")[:-1]
            for img_id in image_list:
                self.images.append(os.path.join(self.img_dir, f"{img_id}.jpg"))

    def preprocess(self, ):
        pass

    def detect(self,):
        # Feature Request, check if we can make this parallel using multiprocessing.
        conf_sum = 0
        detection_count = 0
        img_id_list = []

        # Filter testing images
        if self.only_train == 1:
            # We only evaluate the image that belong to the training_id.txt
            with open(f"./{self.data_root_dir}/testing_id.txt") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                img_id_list.append(line)
        filtered_image_list = []
        for image in self.images:
            if len(img_id_list) != 0:
                # We only evaluate the image that belong to the training_id.txt
                img_id = os.path.basename(image).split("-")[0]
                if img_id in img_id_list:
                    logger.info(f"Find Test Images, Exclude!")
                    continue
            filtered_image_list.append(image)
        logger.info(f"Start Parallel Prediction With {self.jobs} Jobs.")
        # Start parallel prediction
        args = []
        start = 0
        end = len(filtered_image_list)
        chunk_size = int(len(filtered_image_list)/self.jobs) + 1  # we set the chunk size larger so all images can be finished with `self.jobs` processes
        for i in range(start, end, chunk_size):
            images = filtered_image_list[i:i+chunk_size]
            args.append((self.yolo, images, self.save_dir))
        with Pool(self.jobs) as p:
            parallel_result = p.map(model_predict, args)
        for result in parallel_result:
            assert len(result) == 2  # result contains two things: total confidence and total number of detection
            conf_sum += result[0]
            detection_count += result[1]
        if detection_count == 0:
            logger.info(f"AVG Confidence: 0 Count: {detection_count}")
        else:
            logger.info(f"AVG Confidence: {round(conf_sum / detection_count, 2)} Count: {detection_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--source_path', default="./data_company/testing_id.txt", help='Path to image id file')
    parser.add_argument("--img_dir", default="./data_company/ImageSet", type=str, help="The dir of image data")
    parser.add_argument('-w', '--weights_path', default="./data_company/working_dir/origin_model/backup/cross-hands_best.weights", help="Path to model weights")
    parser.add_argument('--save_dir', default="./outputs", help="The dir of yolo output")
    parser.add_argument('-n', '--network', default="normal", choices=["normal", "tiny", "prn", "v4-tiny"],
                        help='Network Type')
    parser.add_argument('-j', '--jobs', default=1, help='Number of parallel jobs')
    parser.add_argument('-d', '--device', default=0, help='Device to use')
    parser.add_argument('-s', '--size', default=416, help='Size for yolo')
    parser.add_argument('-c', '--confidence', default=0.25, help='Confidence for yolo')
    parser.add_argument("--cfg_path", type=str, default="./cfg/cross-hands.cfg", help="The path of configuration")
    parser.add_argument('--only_train', type=int, default=1, help="Whether we only consider the training image")
    parser.add_argument("--dataset", type=str, default="popsquare", help="The type of the dataset")
    flags, unknown = parser.parse_known_args()
    detector = Detector(flags)
    detector.load_weights()
    detector.load_data()
    detector.detect()
