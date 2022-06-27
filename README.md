# Note
Please checkout to the voc branch

# MetaHand
MetaHand is a tool for evaluating and enhancing hand-detection DL models

## How to run
We use YoloV3 model as our target subject, and use darknet for Yolo model training.

To install darknet
```
git clone https://github.com/pjreddie/darknet.git
cd darknet
docker build -f Dockerfile .
docker run --name MetaHand -ti -v /data/{user_name}/Projects/ITF/MetaHand:/root {image_id} 

```

