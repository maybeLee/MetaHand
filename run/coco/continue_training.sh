# This is a utility script to continue training some models for analysis
MutateType=ObjectGaussianMutation
th=0.3
ratio=02
data_dir=data_coco
MutateName=object_gaussian_160_fixMutRatio_centerXY_${ratio}
base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_${th}
WORKDIR=${base_dir}/data
PreTrainedPath=${WORKDIR}/backup/yolov3_best.weights
OBJPATH=${WORKDIR}/obj.data
CFGPATH=${WORKDIR}/yolov3.cfg
GPU=0,1,2
log_dir=logs/coco/testing/${MutateType}
LOGFILE=${log_dir}/${MutateName}_${th}.log
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=0 --pretrained_path=${PreTrainedPath} --gpu=$GPU >> ${LOGFILE}