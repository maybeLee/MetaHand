#!/bin/bash

which_dataset=$1
if [[ ${which_dataset} == "company" ]]
then
    img=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/ImageSet/  #Company dataset原始图像的路径
    label=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/labels/  #Company dataset标签的路径
    mutate=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate/ #Company dataset变异图像的路径
elif [[ ${which_dataset} == "ego" ]]
then
    img=/ssddata/metahand/data_egohands/images/train/   #Public dataset原始图像的路径
    label=/ssddata/metahand/data_egohands/images/train/ #Public dataset标签的路径
    mutate=/ssddata/metahand/data_egohands/mutate/      #Public dataset变异图像的路径
else
    echo "Invalid programme input, expected 'company' or 'ego' but got ${which_dataset}"
    exit 1
fi

mkdir -p $mutate
chmod 777 -R $mutate
for guass_noise in 0.0 0.5 1.0 2.0 4.0 8.0 16.0 32.0 64.0 128.0 
do
    for rand_erase in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 #rmb to set random erase as 0.0 when guassian > 0.0
    do
        apply_guassian=$(awk 'BEGIN{ print "'$guass_noise'"=="'0.0'" }')
        if [ "$apply_guassian" -eq 1 ];then
                o_or_b="object"
        else
                o_or_b="background"
        fi
        echo "running guassian noise ${guass_noise} and randon erase ${rand_erase}, mutation target is ${o_or_b}"
        python -O ../scripts/mutation/mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate \
        --random_erase $rand_erase --random_erase_mode fixMutRatio_centerXY --guassian_sigma $guass_noise \
        --object_or_background $o_or_b
done
done

