# By running this demo scripts, you will train a yolov3 model on egohands dataset by running 10 iterations

cd ../../
TRAIN_ID=./data_egohands/training_id.txt
IMGDIR=./data_egohands/images
LABELDIR=./data_egohands/labels
WORKDIR=./data_egohands/working_dir/demo
GPU=0,1,2
CFGPATH=./cfg/egohands-demo.cfg
OBJPATH=${WORKDIR}/obj.data
DATASET=egohands
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR} --dataset=${DATASET}
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU
