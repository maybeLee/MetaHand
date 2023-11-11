
# MetaHand
MetaHand is a tool for evaluating and enhancing hand-detection DL models

## How to run
We use YOLOv3 and YOLOv7 model as our target subject, and use darknet and pytorch for Yolo model training.

To install darknet
```
git clone https://github.com/pjreddie/darknet.git
cd darknet
docker build -t metahand -f Dockerfile .
docker run --name MetaHand -ti -v /data/{user_name}/Projects/ITF/MetaHand:/root metahand 
# Note that if you are using sccpu6, please add the flag: --security-opt=label=disable on docker run so local dir can be properly mounted
# We also need to compile opencv with GPU for detection (WARNING: don't install opencv from pip, e.g., pip install opencv-python)
docker exec MetaHand bash -c 'cd /root && ./install_opencv.sh'
```

To install YOLOv7 in pytorch's version, remember to clone our project using `git clone --recursive git@github.com:maybeLee/MetaHand.git`

# How to run

### To run some script
All running scripts are stored in the `./run` directory. You can directly run the script outside of the container by:
```
podman exec MetaHand bash -c 'cd /root && ./run/coco/train_coco.sh'
```

# Note

Remember to clone MetaHand under /root/
