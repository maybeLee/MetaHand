#!/bin/bash

which_dataset=$1
if [ ${which_dataset} -eq "company" ]; then 
img=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/ImageSet/
label=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/labels/
mutate=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate/
elif [${which_dataset} -eq "ego"]; then
img=/ssddata/metahand/data_egohands/images/train/
label=/ssddata/metahand/data_egohands/images/train/
mutate=/ssddata/metahand/data_egohands/mutate/
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
for guass_noise in 0.0
do
for rand_erase in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do
    python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode fixMutRatio_centerXY --guassian_sigma $guass_noise --object_or_background $o_or_b 
done
done