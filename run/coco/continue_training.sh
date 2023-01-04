# This is a utility script to continue training some models for analysis
th=0.3
ratio=0.2
data_dir=data_coco
MutateName=object_gaussian_160_fixMutRatio_centerXY_${ratio}
base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_${th}
WORKDIR=${base_dir}/data
PreTrainedPath=${WORKDIR}/backup/yolov3_best.weights
OBJPATH=${WORKDIR}/obj.data
CFGPATH=${WORKDIR}/yolov3.cfg
GPU=0,1,2
LOGFILE={log_dir}/${MutateName}_${th}.log
mkdir -p $LOGDIR
LOGFILE=${LOGDIR}/train_origin.log
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=0 --pretrained_path=${PreTrainedPath} --gpu=$GPU >> ${LOGFILE}