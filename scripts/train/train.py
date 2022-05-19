import os
import argparse
import sys


class Trainer(object):
    def __init__(self, flags):
        self.obj_path = flags.obj_path
        self.cfg_path = flags.cfg_path
        self.pretrained_path = flags.pretrained_path
        self.retrain = flags.retrain
        # obj_path = "data/working_dir/data/obj.data"
        # cfg_path = "./cfg/cross-hands.cfg"

    def train(self, ):
        if self.retrain is False:
            os.system(f"./tools/darknet/darknet detector train {self.obj_path} {self.cfg_path} -dont_show -map")
        elif self.retrain is True and self.pretrained_path is not None:
            os.system(
                f"./tools/darknet/darknet detector train {self.obj_path} {self.cfg_path} {self.pretrained_path} -dont_show -map -clear")



if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--obj_path", type=str, help="The path of objects")
    parse.add_argument("--cfg_path", type=str, help="The path of configuration")
    parse.add_argument("--retrain", type=bool, default=False, help="Whether to retrain the model")
    parse.add_argument("--pretrained_path", type=str, default=None, help="Path of the pretrained model")
    flags, _ = parse.parse_known_args(sys.argv[1:])
    trainer = Trainer(flags)
    trainer.train()
