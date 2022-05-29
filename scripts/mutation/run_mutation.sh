#!/bin/bash

##on server
img=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/ImageSet/
label=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/labels/
mutate=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate/
mkdir -p /data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate
# rand_erase=0.0
# guass_noise=0.0
for rand_erase in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do
for guass_noise in 0.0 0.1 0.5 1.0 2.0 4.0 8.0 16.0
    echo "fixMutRatio_fixXY\n"
    python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode fix_mut_ratio_fixxy --guassian_variance $guass_noise & 
    echo "varyMutRatio_fixXY\n"
    python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode vary_mut_ratio_fixxy --guassian_variance $guass_noise &
    echo "fixMutRatio_varyXY\n"
    python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode fix_mut_ratio_varyxy --guassian_variance $guass_noise &
    echo "varyMutRatio_varyXY\n"
    python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --random_erase_mode vary_mut_ratio_varyxy --guassian_variance $guass_noise &
done
done

# rand_erase=0.0
# for guass_noise in 0.1 0.5 1.0 2.0 4.0 8.0 16.0
# do
#     python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase --guassian_variance $guass_noise
# done
#on window