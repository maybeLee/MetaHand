cd ../../
MutateType=BackgroundGaussianMutation
DATASET=egohands
GPU=0,1,2
data_dir=data_egohands
log_dir=logs/egohands/${MutateType}
weights_path=./${data_dir}/working_dir/origin_model_3000/backup/egohands_best.weights
output_dir=./outputs/egohands
mkdir -p $log_dir
mkdir -p $output_dir
th=0.3
std_list="0_5 1_0 2_0 4_0"
for std in $std_list
do
    MutateName=BackgroundGaussian${std}
    echo "Preparing Data For ${MutateName}"

    python -u -m scripts.evaluation.evaluate \
    -oi=./${data_dir}/images/train \
    -mi=./${data_dir}/${MutateType}/${MutateName} \
    -ol=./${data_dir}/labels \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --threshold=${th} > ${log_dir}/${MutateName}_${th}_3000.log

    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_${th}_3000
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
    --dataset=${DATASET} >> ${log_dir}/${MutateName}_${th}_3000.log

done

gpu_id=0,1,2
for std in $std_list
do
    MutateName=BackgroundGaussian${std}
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_${th}_3000
    CFGPATH=./cfg/egohands.cfg
    WORKDIR=$base_dir/data
    OBJPATH=${WORKDIR}/obj.data
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_${th}_3000
    python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}_${th}_3000.log
done

echo $"Finish All Jobs"

