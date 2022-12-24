# cd ../../
TRAIN_ID=./data_coco/training_id.txt
IMGDIR=./data_coco/coco/images
LABELDIR=./data_coco/coco/labels
WORKDIR=./data_coco/working_dir/testing/origin_model
GPU=2
CFGPATH=./cfg/yolov3.cfg
OBJPATH=${WORKDIR}/obj.data
DATASET=coco
LOGDIR=logs/coco/testing
LOGFILE=${LOGDIR}/train_origin.log
rm -rf ${WORKDIR}
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR} --dataset=${DATASET} > ${LOGFILE}
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU >> ${LOGFILE}
