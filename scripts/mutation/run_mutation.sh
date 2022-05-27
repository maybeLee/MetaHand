#!/bin/bash

##on server
img=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/ImageSet/
label=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/labels/
mutate=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate/
mkdir -p /data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate
python mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate

##on window