cd ../../
TRAIN_ID=./data_voc/training_id.txt
IMGDIR=./data_voc/images
LABELDIR=./data_voc/labels
WORKDIR=./data_voc/working_dir/origin_model_1
GPU=0,1,2
CFGPATH=./cfg/yolov3-voc.cfg
OBJPATH=${WORKDIR}/obj.data
DATASET=voc
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR} --dataset=${DATASET}
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU
