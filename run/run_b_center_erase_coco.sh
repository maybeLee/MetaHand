cd ../
MutateType=CenterEraseMutation
log_dir=logs/coco/${MutateType}
mkdir -p $log_dir
for th in 01 02 03 04 05 06
do
    MutateName=B_random_erase_fixMutRatio_centerXY_${th}
    echo "Preparing Data For ${MutateName}"
    python -u -m scripts.evaluation.evaluate -mi=./data_coco/${MutateType}/$MutateName --threshold=0.3 > ${log_dir}/${MutateName}.log
    base_dir=./data_coco/working_dir/${MutateType}/${MutateName}_th03
    mkdir -p $base_dir
    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt
    python -u -m scripts.train.prepare_train_data --source_path=${base_dir}/${MutateName}_violations.txt \
    --img_dir=./data_coco/${MutateType}/$MutateName --label_dir=empty --target_dir=$base_dir/data_coco >> ${log_dir}/${MutateName}.log
done
gpu_id=0
for th in 01 02
do
    MutateName=B_random_erase_fixMutRatio_centerXY_${th}
    base_dir=./data_coco/working_dir/${MutateType}/${MutateName}_th03
    nohup python -u -m scripts.train.train --obj_path=${base_dir}/data_coco/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log &
    gpu_id=$(($gpu_id+1))
done
MutateName=B_random_erase_fixMutRatio_varyXY_03
base_dir=./data_coco/working_dir/${MutateType}/${MutateName}_th03
python -u -m scripts.train.train --obj_path=${base_dir}/data_coco/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log

gpu_id=0
for th in 04 05 06
do
    MutateName=B_random_erase_fixMutRatio_centerXY_${th}
    base_dir=./data_coco/working_dir/${MutateType}/${MutateName}_th03
    nohup python -u -m scripts.train.train --obj_path=${base_dir}/data_coco/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log &
    gpu_id=$(($gpu_id+1))
done

echo $"Finish All Jobs"
