cd ../
python -u -m scripts.train.prepare_train_data --source_path=./data_coco/training_id.txt --img_dir=./data_coco/ImageSet --label_dir=./data_coco/Labels --target_dir=./data_coco/working_dir/origin_model --dataset=coco
python -u -m scripts.train.train --obj_path=./data_coco/working_dir/origin_model/obj.data --cfg_path=./cfg/yolov3.cfg --retrain=1 --gpu=0
