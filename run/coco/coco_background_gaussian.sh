cd ../
MutateType=BackgroundGaussianMutation
DATASET=coco
GPU=0,1,2
data_dir=data_coco
log_dir=logs/coco/${MutateType}
weights_path=./${data_dir}/working_dir/origin_model/backup/yolov3_best.weights
output_dir=./outputs/coco
mkdir -p $log_dir
mkdir -p $output_dir
for th in 128_0
do
    MutateName=BackgroundGaussian${th}
    echo "Preparing Data For ${MutateName}"

    python -u -m scripts.evaluation.evaluate \
    -oi=./${data_dir}/ImageSet \
    -mi=./${data_dir}/${MutateType}/${MutateName} \
    -ol=./${data_dir}/Labels \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --threshold=0.3 > ${log_dir}/${MutateName}.log

    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_th03
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
    --dataset=${DATASET} >> ${log_dir}/${MutateName}.log

done

gpu_id=0,1,2
for th in 128_0
do
    MutateName=BackgroundGaussian${th}
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_th03
    CFGPATH=./cfg/yolov3.cfg
    WORKDIR=$base_dir/data
    OBJPATH=${WORKDIR}/obj.data
    base_dir=./${data_dir}/working_dir/${MutateType}/${MutateName}_th03
    nohup python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log &
done

echo $"Finish All Jobs"
