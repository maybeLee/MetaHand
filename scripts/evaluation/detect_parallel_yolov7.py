import argparse
import glob
import os
from scripts.utils.logger import Logger
from multiprocessing import Pool
import time


logger = Logger()


def detect_parallel_yolov7(args):
    """
    This function will load the `model` to predict images whose paths are stored in `images`.
    The detection result for each image is stored in save_dir.
    :param args: with the following arguments
    param related data to load model: weights_path, yolo_size, yolo_confidence.
    param related to detection images: dirs of images to be predicted, i_start, i_end
    param save_dir: directory to save the prediction result
    :return: total number of detection
    """
    weights_path, yolo_size, yolo_confidence, img_dir, i_start, i_end, save_dir, base_name = args
    weights_path = weights_path.replace("tools/yolov7/", "")
    img_dir = img_dir.replace("tools/yolov7/", "")
    os.system(f"cd tools/yolov7/;python detect.py --weights {weights_path} "
              f"--source {img_dir} --img-size {yolo_size} --name {base_name} --i_start {i_start} --i_end {i_end} --save-txt --increment_path >/dev/null 2>&1;cd ../../")


class Detector(object):
    def __init__(self, flags):
        self.source_path = flags.img_dir
        self.yolo_size = flags.size
        self.yolo_confidence = flags.confidence
        self.jobs = flags.jobs
        self.img_dir = flags.img_dir.rstrip("/")
        self.base_name = os.path.basename(self.img_dir.rstrip("/*"))
        self.save_dir = flags.save_dir.rstrip("/")
        self.weights_path = flags.weights_path
        self.images = []
        self.initiate_dirs()

    def initiate_dirs(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def load_data(self, ):
        """
        Load images stored in `self.img_dir` to detect, the image paths will be stored in list, e.g., [path1, path2, ...]
        :return: None
        """
        self.img_dir.rstrip("*")
        self.images = sorted(glob.glob(os.path.join(self.img_dir, '*.*')))  # dir

    def detect(self,):
        logger.info(f"Start Parallel Prediction With {self.jobs} Jobs.")
        s_time = time.time()

        # Start parallel prediction
        args = []
        start = 0
        chunk_size = int(len(self.images)/self.jobs) + 1  # we set the chunk size larger so all images can be finished with `self.jobs` processes
        for i in range(start, len(self.images), chunk_size):
            i_start = i
            i_end = i+chunk_size
            args.append(
                (
                    self.weights_path, self.yolo_size, self.yolo_confidence,
                    self.img_dir, i_start, i_end, self.save_dir, self.base_name
                )
            )
        with Pool(self.jobs) as p:
            parallel_result = p.map(detect_parallel_yolov7, args)
        logger.info("Finish detecting, merging the detection results")
        e_time = time.time()
        logger.info(f"Total Time Used: {e_time - s_time}")

    def detect_single(self):
        args = (self.weights_path, self.yolo_size, self.yolo_confidence, self.img_dir, None, None, self.save_dir, self.base_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", default="./tools/yolov7/coco/images/train2017", type=str, help="The dir of image data")
    parser.add_argument('-w', '--weights_path', default="./tools/yolov7/runs/train/yolov7/weights/best.pt", help="Path to model weights")
    parser.add_argument('--save_dir', default="./outputs", help="The dir of yolo output")
    parser.add_argument('-j', '--jobs', type=int, default=1, help='Number of parallel jobs')
    parser.add_argument('-d', '--device', default=0, help='Device to use')
    parser.add_argument('-s', '--size', default=320, help='Size for yolo')
    parser.add_argument('-c', '--confidence', default=0.25, help='Confidence for yolo')
    flags, unknown = parser.parse_known_args()
    detector = Detector(flags)
    detector.load_data()
    detector.detect()

