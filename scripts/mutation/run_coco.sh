#!/bin/bash
python -O coco_convert_and_mutate.py --source_image_path /data/litszon/coco_source_data/test2017/ \
--source_label_path /data/litszon/coco_source_data/annotations/ \
--working_dir_path /ssddata/metahand/coco/ \
--object_category person