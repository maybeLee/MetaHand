cd ../
python -u -m scripts.train.prepare_train_data --source_path=./data/training_id.txt --img_dir=./data/ImageSet --label_dir=./data/Labels --target_dir=./data/working_dir/origin_model_1
python -u -m scripts.train.train --obj_path=./data/working_dir/origin_model_1/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1 --gpu=0
