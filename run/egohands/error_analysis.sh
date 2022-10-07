cd ../../
MutateType=BackgroundGaussianMutation
DATASET=egohands
GPU=0,1,2
data_dir=data_egohands
weights_path=./${data_dir}/working_dir/testing/origin_model/backup/egohands_best.weights
output_dir=./outputs/egohands
th=0.3
std_list="2_0"
for std in $std_list
do
    MutateName=BackgroundGaussian${std}
    echo "Preparing Data For ${MutateName}"

    python -u -m scripts.evaluation.error_analysis \
    -oi=./${data_dir}/images/train \
    -mi=./${data_dir}/${MutateType}/${MutateName} \
    -ol=./${data_dir}/labels \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --threshold=${th}
done

echo $"Finish All Jobs"

