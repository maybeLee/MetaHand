cd ../
MutateType=CenterEraseMutation
log_dir=logs/${MutateType}
mkdir -p $log_dir
for MutateName in B_random_erase_fixMutRatio_centerXY_01 B_random_erase_fixMutRatio_centerXY_02 B_random_erase_fixMutRatio_centerXY_03 B_random_erase_fixMutRatio_centerXY_04
do
    echo "Preparing Data For ${MutateName}"
    python -u -m scripts.evaluation.evaluate -mi=./data/${MutateType}/$MutateName --threshold=0.05 > ${log_dir}/${MutateName}_th005.log
    base_dir=./data/working_dir/${MutateType}/${MutateName}_th005
    mkdir -p $base_dir
    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt
    python -u -m scripts.train.prepare_train_data --source_path=${base_dir}/${MutateName}_violations.txt \
    --img_dir=./data/${MutateType}/$MutateName --label_dir=empty --target_dir=$base_dir/data >> ${log_dir}/${MutateName}_th005.log
done
gpu_id=0
for MutateName in B_random_erase_fixMutRatio_centerXY_01 B_random_erase_fixMutRatio_centerXY_02
do
    base_dir=./data/working_dir/${MutateType}/${MutateName}_th005
    nohup python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}_th005.log &
    gpu_id=$(($gpu_id+1))
done
MutateName=B_random_erase_fixMutRatio_centerXY_03
base_dir=./data/working_dir/${MutateType}/${MutateName}_th005
python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}_th005.log

gpu_id=0
for MutateName in B_random_erase_fixMutRatio_centerXY_04
do
    base_dir=./data/working_dir/${MutateType}/${MutateName}_th005
    nohup python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}_th005.log &
    gpu_id=$(($gpu_id+1))
done

echo $"Finish All Jobs"
