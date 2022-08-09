cd ../../
MutateType=ObjectGaussianMutation
ratio_list="01 02 03 04 05 06 07 08 09"
for ratio in $ratio_list
do
    MutateName=B_guassian_160_fixMutRatio_centerXY_${ratio}
    echo "Working on ${MutateName}"
    output_dir=outputs/company/repair/${MutateName}/
    mkdir -p $output_dir
    echo "Preparing Data For ${MutateName}"
    base_dir=./data_company/working_dir/${MutateType}/${MutateName}_th03
    weights_path=${base_dir}/data/backup/cross-hands_best.weights
    origin_weights_path=./data_company/working_dir/origin_model/backup/cross-hands_best.weights
    python -u -m scripts.evaluation.compare -ow=${origin_weights_path} -rw=${weights_path} -l=./data_company/Labels -i=./data_company/ImageSet -od=${output_dir} -ood=./outputs/company/
    mv target.txt ${output_dir}
done
echo $"Finish All Jobs"
