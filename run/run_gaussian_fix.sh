cd ../
MutateType=GaussianFixMutation
log_dir=logs/${MutateType}
mkdir -p $log_dir
for MutateRatio in 07 08 09
do
    MutateName=B_guassian_160_fixMutRatio_fixXY_${MutateRatio}
    echo "Preparing Data For ${MutateName}"
    python -u -m scripts.evaluation.evaluate -mi=./data/${MutateType}/$MutateName --threshold=0.3 > ${log_dir}/${MutateName}.log
    base_dir=./data/working_dir/${MutateType}/${MutateName}_th03
    mkdir -p $base_dir
    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt
    python -u -m scripts.train.prepare_train_data --source_path=${base_dir}/${MutateName}_violations.txt \
    --img_dir=./data/${MutateType}/$MutateName --label_dir=same --target_dir=$base_dir/data >> ${log_dir}/${MutateName}.log
done
gpu_id=0
for MutateName in B_guassian_160_fixMutRatio_fixXY_07 B_guassian_160_fixMutRatio_fixXY_08 B_guassian_160_fixMutRatio_fixXY_09
do
    base_dir=./data/working_dir/${MutateType}/${MutateName}_th03
    nohup python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log &
    gpu_id=$(($gpu_id+1))
done
# MutateName=B_guassian_160_fixMutRatio_fixXY_03
# base_dir=./data/working_dir/${MutateType}/${MutateName}_th03
# python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log

# gpu_id=0
# for MutateName in B_guassian_160_fixMutRatio_fixXY_04 B_guassian_160_fixMutRatio_fixXY_05 B_guassian_160_fixMutRatio_fixXY_06
# do
#     base_dir=./data/working_dir/${MutateType}/${MutateName}_th03
#     nohup python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log &
#     gpu_id=$(($gpu_id+1))
# done

echo $"Finish All Jobs"
