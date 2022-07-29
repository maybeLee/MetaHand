cd ../../
MutateType=ObjectGaussianMutation
log_dir=logs/company/${MutateType}
output_dir=outputs/company
mkdir -p $log_dir
mkdir -p $output_dir
# std_list="1_0 2_0 4_0 8_0 16_0 32_0 64_0 128_0"
ratio_list="01 02 03 04 05 06 07 08 09"
# for std in $std_list
for ratio in $ratio_list
do
    MutateName=B_guassian_160_fixMutRatio_centerXY_${ratio}
    echo "Preparing Data For ${MutateName}"
    
    python -u -m scripts.evaluation.evaluate -mi=./data_company/${MutateType}/$MutateName -od=${output_dir} --threshold=0.3 > ${log_dir}/${MutateName}.log
    base_dir=./data_company/working_dir/${MutateType}/${MutateName}_th03
    mkdir -p $base_dir
    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt
    python -u -m scripts.train.prepare_train_data --source_path=${base_dir}/${MutateName}_violations.txt \
    --img_dir=./data_company/${MutateType}/$MutateName --label_dir=same --target_dir=$base_dir/data >> ${log_dir}/${MutateName}.log
done

gpu_id=0,1,2
# for std in $std_list
for ratio in $ratio_list
do
    MutateName=B_guassian_160_fixMutRatio_centerXY_${ratio}
    base_dir=./data_company/working_dir/${MutateType}/${MutateName}_th03
    python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=$gpu_id >> ${log_dir}/${MutateName}.log
done

echo $"Finish All Jobs"
