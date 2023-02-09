# cd ../../
TRAIN_ID=./data_imagenet/training_id.txt
IMGDIR=./data_imagenet/images
LABELDIR=./data_imagenet/labels
WORKDIR=./data_imagenet/working_dir/testing/origin_model
GPU=0,1,2
num_epoch=100
original_cfg_path=./cfg/yolov3-imagenet.cfg
CFGPATH=${WORKDIR}/yolov3.cfg
OBJPATH=${WORKDIR}/obj.data
DATASET=imagenet
LOGDIR=logs/imagenet/testing
mkdir -p $LOGDIR
LOGFILE=${LOGDIR}/train_origin.log
rm -rf ${WORKDIR}
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR} --dataset=${DATASET} --num_epoch=$num_epoch --cfg_path=$original_cfg_path > ${LOGFILE}
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU >> ${LOGFILE}
