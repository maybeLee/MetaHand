cd ../
WorkDir=CenterEraseGaussian
log_dir=logs/${WorkDir}
mkdir -p $log_dir
for th in 07 08 09
do
    GaussianName=B_guassian_160_varyMutRatio_varyXY_$th
    CenterEraseName=B_random_erase_fixMutRatio_centerXY_$th
    WorkName=${GaussianName}_${CenterEraseName}
    rm -rf ${log_dir}/${WorkName}.log
    base_dir=./data/working_dir/${WorkDir}/${WorkName}_th03
    mkdir -p $base_dir

    MutateType=GaussianVaryMutation
    python -u -m scripts.evaluation.evaluate -mi=./data/${MutateType}/$GaussianName --threshold=0.3 >> ${log_dir}/${WorkName}.log
    mv ${GaussianName}_violations.txt ${base_dir}/${GaussianName}_violations.txt
    python -u -m scripts.train.prepare_train_data --source_path=${base_dir}/${GaussianName}_violations.txt \
    --img_dir=./data/${MutateType}/${GaussianName} --label_dir=same --target_dir=$base_dir/data --append=0 >> ${log_dir}/${WorkName}.log

    # For CenterErase, do remember to append the data without removing the original
    MutateType=CenterEraseMutation
    python -u -m scripts.evaluation.evaluate -mi=./data/${MutateType}/$CenterEraseName --threshold=0.3 >> ${log_dir}/${WorkName}.log
    mv ${CenterEraseName}_violations.txt ${base_dir}/${CenterEraseName}_violations.txt
    python -u -m scripts.train.prepare_train_data --source_path=${base_dir}/${CenterEraseName}_violations.txt \
    --img_dir=./data/${MutateType}/${CenterEraseName} --label_dir=empty --target_dir=$base_dir/data --append=1 >> ${log_dir}/${WorkName}.log
done
WorkDir=CenterEraseGaussian
gpu_id=0
for th in 07 08 09
do
    GaussianName=B_guassian_160_varyMutRatio_varyXY_$th
    CenterEraseName=B_random_erase_fixMutRatio_centerXY_$th
    WorkName=${GaussianName}_${CenterEraseName}
    base_dir=./data/working_dir/${WorkDir}/${WorkName}_th03
    nohup python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${WorkName}.log &
    gpu_id=$(($gpu_id+1))
done

# th=03
# GaussianName=B_guassian_160_varyMutRatio_varyXY_$th
# CenterEraseName=B_random_erase_fixMutRatio_centerXY_$th
# WorkName=${GaussianName}_${CenterEraseName}
# base_dir=./data/working_dir/${WorkDir}/${WorkName}_th03
# python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${WorkName}.log

# gpu_id=0
# for th in 04 05 06
# do
#     GaussianName=B_guassian_160_varyMutRatio_varyXY_$th
#     CenterEraseName=B_random_erase_fixMutRatio_centerXY_$th
#     WorkName=${GaussianName}_${CenterEraseName}
#     base_dir=./data/working_dir/${WorkDir}/${WorkName}_th03
#     nohup python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${WorkName}.log &
#     gpu_id=$(($gpu_id+1))
# done

echo $"Finish All Jobs"
