cd ../../
MutateType=BackgroundGaussianMutation
DATASET=voc
GPU=0,1,2
data_dir=data_voc
log_dir=logs/voc/${MutateType}
weights_path=./${data_dir}/working_dir/origin_model/backup/yolov3-voc_best.weights
output_dir=./outputs/voc
mkdir -p $log_dir
mkdir -p $output_dir
# finished: 0.3 0.8
std=64_0
for th in 0.1 0.2 0.4 0.5 0.6 0.7 0.9
do
    MutateName=BackgroundGaussian${std}
    echo "Preparing Data For ${MutateName}"

    python -u -m scripts.evaluation.evaluate \
    -oi=./${data_dir}/images/train2014 \
    -mi=./${data_dir}/${MutateType}/${MutateName} \
    -ol=./${data_dir}/labels/train2014 \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --threshold=${th} > ${log_dir}/${MutateName}_${th}.log

    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_${th}
    mkdir -p $base_dir
    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt

    TRAIN_ID=${base_dir}/${MutateName}_violations.txt
    IMGDIR=./${data_dir}/${MutateType}/$MutateName
    LABELDIR=same
    WORKDIR=$base_dir/data

    python -u -m scripts.train.prepare_train_data \
    --source_path=${TRAIN_ID} \
    --img_dir=${IMGDIR} \
    --label_dir=${LABELDIR} \
    --target_dir=${WORKDIR} \
    --dataset=${DATASET} >> ${log_dir}/${MutateName}_${th}.log

done

gpu_id=0,1,2
for th in 0.1 0.2 0.4 0.5 0.6 0.7 0.9
do
    MutateName=BackgroundGaussian${std}
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_${th}
    CFGPATH=./cfg/yolov3-voc.cfg
    WORKDIR=$base_dir/data
    OBJPATH=${WORKDIR}/obj.data
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_${th}
    python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}_${th}.log
done

echo $"Finish All Jobs"

