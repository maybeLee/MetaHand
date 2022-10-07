#!/bin/bash
#./mutate.sh company > log_company.out 2> log_company.err
which_dataset=$1
if [[ ${which_dataset} == "company" ]]
then
    img=/root/data_company/ImageSet/  #Company dataset原始图像的路径
    label=/root/data_company/Labels/  #Company dataset标签的路径
    mutate=/root/data_company/ObjactGaussianMutation/ #Company dataset变异图像的路径
elif [[ ${which_dataset} == "ego" ]]
then
    img=/root/data_egohands/ImageSet/   #Public dataset原始图像的路径
    label=/root/data_egohands/Labels/ #Public dataset标签的路径
    mutate=/root/data_egohands/ObjactGaussianMutation/      #Public dataset变异图像的路径
else
    echo "Invalid programme input, expected 'company' or 'ego' but got ${which_dataset}"
    exit 1
fi

mkdir -p $mutate
chmod 777 -R $mutate
# mkdir -p ${mutate}
# mkdir -p ${mutate}log #for recording which process finishes during multi-processing
# rand_erase=0.0
# guass_noise=0.0
# for guass_noise in 0.0 0.5 1.0 2.0 4.0 8.0 16.0 32.0 64.0 128.0
for guass_noise in 128.0 16.0 32.0 64.0 
do
for rand_erase in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
do
    apply_guassian=$(awk 'BEGIN{ print "'$guass_noise'"=="'0.0'" }')
    if [ "$apply_guassian" -eq 1 ];then
        o_or_b="object" #gaussian equals 0
    else
        guassian_on_object=$(awk 'BEGIN{ print "'$rand_erase'"=="'0.0'" }')
        if [ "$apply_guassian" -eq 1 ];then
            o_or_b="background" #random ratio equals 0, which means apply guassian to background
        else
            o_or_b="object"
            fi
    fi
    echo "running guassian noise ${guass_noise} and randon erase ${rand_erase}, mutation target is ${o_or_b}"
    python -O ./scripts/mutation/mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode fixMutRatio_centerXY --guassian_sigma $guass_noise --object_or_background $o_or_b --dataset ${which_dataset}
done
done

