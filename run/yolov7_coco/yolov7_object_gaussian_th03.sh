cd ../../
MutateType=ObjectGaussianMutation
DATASET=yolov7
GPU=0,1,2
data_dir=tools/yolov7/coco
log_dir=logs/yolov7/${MutateType}
weights_path=./tools/yolov7/runs/train/yolov7/weights/best.pt
output_dir=./tools/yolov7/runs/detect
mkdir -p $log_dir
mkdir -p $output_dir
th=0.3
# std_list="1_0 2_0 4_0 8_0 16_0 32_0 64_0 128_0"
ratio_list="03"
# for std in $std_list
for ratio in $ratio_list
do
    MutateName=object_gaussian_160_fixMutRatio_centerXY_${ratio}
    MR=2
    LABELDIR=same
    echo "Preparing Data For ${MutateName}"

    python -u -m scripts.evaluation.evaluate \
    -oi=./${data_dir}/images/train2017 \
    -mi=./${data_dir}/${MutateType}/${MutateName} \
    -ol=./${data_dir}/labels/train2017 \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --mr=${MR} \
    --jobs=8 \
    --threshold=${th} > ${log_dir}/${MutateName}_${th}.log

#    base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_${th}
#    mkdir -p $base_dir
#    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt
#
#    TRAIN_ID=${base_dir}/${MutateName}_violations.txt
#    IMGDIR=./${data_dir}/${MutateType}/$MutateName
#    WORKDIR=$base_dir/data
#
#    python -u -m scripts.train.prepare_train_data \
#    --source_path=${TRAIN_ID} \
#    --img_dir=${IMGDIR} \
#    --label_dir=${LABELDIR} \
#    --target_dir=${WORKDIR} \
#    --dataset=${DATASET} --num_epoch=$num_epoch --cfg_path=$original_cfg_path >> ${log_dir}/${MutateName}_${th}.log

done

#gpu_id=0,1,2
#for ratio in $ratio_list
#do
#    MutateName=object_gaussian_160_fixMutRatio_centerXY_${ratio}
#    base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_${th}
#    WORKDIR=$base_dir/data
#    CFGPATH=${WORKDIR}/yolov3.cfg
#    OBJPATH=${WORKDIR}/obj.data
#    base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_${th}
#    python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}_${th}.log
#done

echo $"Finish All Jobs"

