cd ../../
MutateType=CenterEraseMutation
DATASET=egohands
GPU=0,1,2
data_dir=data_egohands
log_dir=logs/egohands/${MutateType}
weights_path=./${data_dir}/working_dir/testing/origin_model/backup/egohands_best.weights
output_dir=./outputs/egohands
mkdir -p $log_dir
mkdir -p $output_dir
th_list="01 02 03 04 05 06 07 08 09"
for th in $th_list
do
    MutateName=B_random_erase_fixMutRatio_centerXY_${th}
    echo "Preparing Data For ${MutateName}"

    python -u -m scripts.evaluation.evaluate \
    -oi=./${data_dir}/images/train \
    -mi=./${data_dir}/${MutateType}/${MutateName} \
    -ol=./${data_dir}/labels \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --threshold=0.3 > ${log_dir}/${MutateName}.log

    base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_th03
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
for th in $th_list
do
    MutateName=B_random_erase_fixMutRatio_centerXY_${th}
    base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_th03
    CFGPATH=./cfg/egohands.cfg
    WORKDIR=$base_dir/data
    OBJPATH=${WORKDIR}/obj.data
    base_dir=./${data_dir}/working_dir/testing/${MutateType}/${MutateName}_th03
    python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log
done

echo $"Finish All Jobs"
