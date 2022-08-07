cd ../../
TRAIN_ID=./data_egohands/training_id.txt
IMGDIR=./data_egohands/images
LABELDIR=./data_egohands/labels
WORKDIR=./data_egohands/working_dir/origin_model
GPU=0,1,2
CFGPATH=./cfg/egohands.cfg
OBJPATH=${WORKDIR}/obj.data
DATASET=egohands
LOGDIR=logs/egohands
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR} --dataset=${DATASET} > ${LOGDIR}/train_origin.log
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU >> ${LOGDIR}/train_origin.log