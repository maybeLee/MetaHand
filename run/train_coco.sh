cd ../
TRAIN_ID=./data_coco/training_id.txt
WORKDIR=./data_coco/working_dir/origin_model
GPU=0,1,2
CFGPATH=./cfg/yolov3.cfg
OBJPATH=${WORKDIR}/obj.data
DATASET=coco
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR} --dataset=${DATASET}
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU
