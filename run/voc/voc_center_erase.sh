cd ../../
MutateType=CenterEraseMutation
DATASET=voc
GPU=0,1,2
data_dir=data_voc
log_dir=logs/voc/${MutateType}
weights_path=./${data_dir}/working_dir/origin_model/backup/yolov3-voc_best.weights
output_dir=./outputs/voc
mkdir -p $log_dir
mkdir -p $output_dir
# finished run: th=08 01 03 05 07 09
for th in 02 04 06
do
    MutateName=B_random_erase_fixMutRatio_centerXY_${th}
    echo "Preparing Data For ${MutateName}"

    python -u -m scripts.evaluation.evaluate \
    -oi=./${data_dir}/images/train2014 \
    -mi=./${data_dir}/${MutateType}/${MutateName} \
    -ol=./${data_dir}/labels/train2014 \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --threshold=0.3 > ${log_dir}/${MutateName}.log

    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_th03
    mkdir -p $base_dir
    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt

    TRAIN_ID=${base_dir}/${MutateName}_violations.txt
    IMGDIR=./${data_dir}/${MutateType}/$MutateName
    LABELDIR=empty
    WORKDIR=$base_dir/data

    python -u -m scripts.train.prepare_train_data \
    --source_path=${TRAIN_ID} \
    --img_dir=${IMGDIR} \
    --label_dir=${LABELDIR} \
    --target_dir=${WORKDIR} \
    --dataset=${DATASET} >> ${log_dir}/${MutateName}.log

done

gpu_id=0,1,2
for th in 02 04 06
do
    MutateName=B_random_erase_fixMutRatio_centerXY_${th}
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_th03
    CFGPATH=./cfg/yolov3-voc.cfg
    WORKDIR=$base_dir/data
    OBJPATH=${WORKDIR}/obj.data
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_th03
    python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log
done

echo $"Finish All Jobs"
