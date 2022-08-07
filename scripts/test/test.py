import os
import argparse
import sys
from scripts.utils.logger import Logger
import time
logger = Logger()


class Tester(object):
    def __init__(self, flags):
        self.obj_path = flags.obj_path
        self.cfg_path = flags.cfg_path
        self.weights_path = flags.weights_path
        self.gpu = flags.gpu

    def test(self, ):
        logger.info(f"Evaluating weights: {self.weights_path}")
        os.system(f"./tools/darknet/darknet detector map {self.obj_path} {self.cfg_path} {self.weights_path} -gpus {self.gpu} -dont_show -ext_output")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--obj_path", type=str, help="The path of objects")
    parser.add_argument("--cfg_path", type=str, help="The path of configuration")
    parser.add_argument("--weights_path", type=str, default=None, help="Path of the pretrained model")
    parser.add_argument("--gpu", type=str, default="1", help="Specify the gpu id")  # note that in the docker environment, 0 gpu id means the 1 actual gpu id
    flags, _ = parser.parse_known_args(sys.argv[1:])
    tester = Tester(flags)
    tester.test()
