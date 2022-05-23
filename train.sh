python -u -m scripts.train.prepare_train_data --source_path=./data/training_id.txt --img_dir=./data/ImageSet --label_dir=./data/Labels --target_dir=./data/working_dir/exp220522/origin_model
python -u -m scripts.train.train --obj_path=./data/working_dir/origin_model/obj.data --cfg_path=./data/working_dir/exp220522/cross-hands.cfg --retrain=1 --gpu=0
