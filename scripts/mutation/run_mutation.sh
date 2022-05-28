#!/bin/bash

##on server
img=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/ImageSet/
label=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/labels/
mutate=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate/
mkdir -p /data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate
for rand_erase in 0.5 0.6 0.7 0.8 0.9 1.0
do
    python -O mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate --random_erase $rand_erase
done
##on window