#!/bin/bash
img=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/ImageSet
label_path=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/labels
mutate_path=/data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate
mkdir -c /data/litszon/itf/ITF/2165-143-89-238-111.ap.ngrok.io/mutate
python mutation_operation.py --image_path $img --label_path $label --mutate_path $mutate