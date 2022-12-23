cd ../../
MutateType=ObjectGaussianMutation
output_dir=./backup/outputs/company
mkdir -p $output_dir
ratio_list="03"
for ratio in $ratio_list
do
    MutateName=B_guassian_160_fixMutRatio_centerXY_${ratio}
    echo "Preparing Data For ${MutateName}"
    python -u -m scripts.evaluation.error_analysis -mi=./data_company/${MutateType}/$MutateName -od=${output_dir} --threshold=0.3
done

echo $"Finish All Jobs"
