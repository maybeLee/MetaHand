#!/bin/bash

##on server
# img=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/ImageSet/
# label=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/labels/
# mutate=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate/

img=/ssddata/metahand/coco/images
label=/ssddata/metahand/coco/labels
mutate=/ssddata/metahand/coco/mutate

mkdir -p /ssddata/metahand/coco/mutate
mkdir -p /ssddata/metahand/coco/mutate/log #for recording which process finishes during multi-processing
# rand_erase=0.0
# guass_noise=0.0
# for guass_noise in 0.0 0.1 0.5 1.0 2.0 4.0 8.0 16.0
for guass_noise in 0.0
do
for rand_erase in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do
    # echo "fixMutRatio_fixXY\n"
    python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode fixMutRatio_centerXY --guassian_variance $guass_noise & 
    # echo "varyMutRatio_fixXY\n"
    # python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode varyMutRatio_fixXY --guassian_variance $guass_noise &
    # echo "fixMutRatio_varyXY\n"
    # python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode fixMutRatio_varyXY --guassian_variance $guass_noise &
    # echo "varyMutRatio_varyXY\n"
    # python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode varyMutRatio_varyXY --guassian_variance $guass_noise &
done
done

# rand_erase=0.0
# for guass_noise in 0.1 0.5 1.0 2.0 4.0 8.0 16.0
# do
#     python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --guassian_variance $guass_noise
# done
#on window