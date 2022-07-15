import os
import argparse
import sys
from scripts.utils.logger import Logger
logger = Logger()


class Trainer(object):
    def __init__(self, flags):
        self.obj_path = flags.obj_path
        self.cfg_path = flags.cfg_path
        self.pretrained_path = flags.pretrained_path
        self.retrain = flags.retrain
        self.gpu = flags.gpu

    def train(self, ):
        logger.info(f"{self.retrain}, {self.pretrained_path}, {self.gpu}")
        if self.retrain == 1:
            os.system(f"./tools/darknet/darknet detector train {self.obj_path} {self.cfg_path} -gpus {self.gpu} -dont_show -map -clear")
        elif self.retrain == -1:
            os.system(f"./tools/darknet/darknet detector test {self.obj_path} {self.cfg_path} -gpus {self.gpu} -dont_show -map -clear")
        elif self.retrain == 0 and self.pretrained_path is not None:
            logger.info("Continue Training")
            os.system(
                f"./tools/darknet/darknet detector train {self.obj_path} {self.cfg_path} {self.pretrained_path} -dont_show -map")
        else:
            raise ValueError(f"Unknown Training Option! retrain: {self.retrain}, pretrained_path: {self.pretrained_path}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--obj_path", type=str, help="The path of objects")
    parser.add_argument("--cfg_path", type=str, help="The path of configuration")
    parser.add_argument("--retrain", type=int, default=0, help="Whether to retrain the model")
    parser.add_argument("--pretrained_path", type=str, default=None, help="Path of the pretrained model")
    parser.add_argument("--gpu", type=str, default="1", help="Specify the gpu id")  # note that in the docker environment, 0 gpu id means the 1 actual gpu id
    flags, _ = parser.parse_known_args(sys.argv[1:])
    trainer = Trainer(flags)
    trainer.train()
