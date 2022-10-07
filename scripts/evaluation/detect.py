import argparse
import glob
import os
import time
import cv2
import numpy as np
from scripts.evaluation.yolo import YOLO
from scripts.utils.logger import Logger
logger = Logger()


class Detector(object):
    def __init__(self, flags):
        self.yolo = None
        self.yolo_cfg = "./cfg/cross-hands.cfg"
        self.yolo_size = flags.size
        self.yolo_confidence = flags.confidence
        self.source_path = flags.source_path
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
        self.yolo = YOLO(self.yolo_cfg, self.weights_path, ["hand"])
        self.yolo.size = int(self.yolo_size)
        self.yolo.confidence = float(self.yolo_confidence)

    def load_data(self, ):
        logger.info("Loading Images...")
        if self.source_path == "all":
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
        # TODO: Currently this method is slow, not sure if it is caused by YOLO inference or frequent I/O.
        #  Need to Check.
        conf_sum = 0
        detection_count = 0
        total_num = len(self.images)
        img_id_list = []
        if self.only_train == 1:
            # We only evaluate the image that belong to the training_id.txt
            with open("./data_company/testing_id.txt") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                img_id_list.append(line)
        for i, image in enumerate(self.images):
            logger.info(f"Iteration: {i}/{total_num}")
            img_id = os.path.basename(image).split("-")[0]
            if len(img_id_list) != 0:
                # We only evaluate the image that belong to the training_id.txt
                img_id = os.path.basename(image).split("-")[0]
                if img_id in img_id_list:
                    logger.info(f"Find Test Images, Exclude!")
                    continue
            mat = cv2.imread(image)
            width, height, inference_time, results = self.yolo.inference(mat)
            # print("%s in %s seconds: %s classes found!" % (os.path.basename(file), round(inference_time, 2), len(results)))
            output = []
            # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            # cv2.resizeWindow('image', 848, 640)
            res_path = os.path.join(self.save_dir, f"{os.path.basename(image)[:-4]}.txt")
            label_path = os.path.join(self.save_dir, f"{os.path.basename(image)[:-4]}_label.jpg")
            with open(res_path, "a") as file:
                for res in results:
                    id, name, confidence, x, y, w, h = res

                    file.write("%s %s %s %s %s %s\n" % (
                    '0', str(x / width), str(y / height), str(w / width), str(h / height), str(confidence)))

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

                    # print("%s with %s confidence" % (name, round(confidence, 2)))

                cv2.imwrite(label_path, mat)
                # show the output image
                # cv2.imshow('image', mat)
                # cv2_imshow(mat)
                # here cv2.waitKey(0)
        logger.info(f"AVG Confidence: {round(conf_sum / detection_count, 2)} Count: {detection_count}")
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--source_path', default="./data_company/testing_id.txt", help='Path to image id file')
    parser.add_argument("--img_dir", default="./data_company/ImageSet", type=str, help="The dir of image data")
    parser.add_argument('-w', '--weights_path', default="./data_company/working_dir/origin_model/backup/cross-hands_best.weights", help="Path to model weights")
    parser.add_argument('--save_dir', default="./outputs", help="The dir of yolo output")
    parser.add_argument('-n', '--network', default="normal", choices=["normal", "tiny", "prn", "v4-tiny"],
                        help='Network Type')
    parser.add_argument('-d', '--device', default=0, help='Device to use')
    parser.add_argument('-s', '--size', default=416, help='Size for yolo')
    parser.add_argument('-c', '--confidence', default=0.25, help='Confidence for yolo')
    parser.add_argument('--only_train', type=int, default=1, help="Whether we only consider the training image")
    flags, unknown = parser.parse_known_args()
    detector = Detector(flags)
    detector.load_weights()
    detector.load_data()
    detector.detect()
