Data/Model for Coco Object Detection Task.

Training Image Set: ./coco/images/train2014/, the path of all training images are determined in training_id.txt (trainvalno5k.txt in darknet)
Validation Image Set: ./coco/images/val2014/, note that in our task, we use consider validation set as the test set. We use the mAP in validation set as the metric to evaluate the performance of trained model, the path of all testing images are determined in testing_id.txt (5k.txt in darknet)
collect_size_of_coco_imgs.py: code used to analyze the size (width, height, channel) of each image in coco
img_size.log: log the size of each image in coco
images: directory containing all training images (117264)
labels: directory containing all training lables (117264)

