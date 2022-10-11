# mutated images: /ssddata1/users/dlproj/MetaHand/data_company/ImageSet/10108152.jpg
# mutation type: objectgaussian
import os
import sys
import subprocess

class DEMO(object):
    def __init__(self):
        self.original_model_path = "/ssddata1/users/dlproj/MetaHand/data_company/working_dir/origin_model/backup/cross-hands_best.weights"
        pass
    
    def test_model(self, working_dir):
        obj_path=f"{working_dir}/obj.data"
        cfg_path="./cfg/cross-hands.cfg"
        weights_path=f"{working_dir}/backup/cross-hands_best.weights"
        gpu="0,1,2"
        subprocess.call(f"podman exec -it suspicious_davinci /bin/bash -c 'cd /root; python -u -m scripts.test.test --obj_path={obj_path} --cfg_path={cfg_path} --weights_path={weights_path} --gpu={gpu}'", shell=True, stdout=sys.stdout)
    
    def check_inference(self):
        pass

    def evaluate_repair(self):
        pass

    def detect_image(self, weights_path, img_path):
        save_dir="./demo/images"
        status = subprocess.call(f"podman exec -it suspicious_davinci /bin/bash -c 'cd /root; python -u -m scripts.evaluation.detect -i=all --img_dir={img_path} -w={weights_path} --save_dir={save_dir}'", shell=True)

