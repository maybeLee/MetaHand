#!/bin/bash
# python -O coco_convert_and_mutate.py --source_image_path /data/litszon/coco_source_data/train2017/ \
# --source_label_path /data/litszon/coco_source_data/annotations/ \
# --working_dir_path /ssddata/metahand/coco/ \
# --json instances_train2017.json 

# for voc
python -O coco_convert_and_mutate.py --source_image_path /data/litszon/itf/VOCdevkit/VOC2012/JPEGImages/ \
--source_label_path /data/litszon/itf/VOCdevkit/VOC2012/Annotations/ \
--working_dir_path /ssddata/metahand/voc/ \
--json dummy --dataset voc