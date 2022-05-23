python -u -m scripts.train.prepare_train_data --source_path=./data/working_dir/aug_id.txt --img_dir=./data/MutatedSet/objects --label_dir=./data/MutatedSet/labels --target_dir=./data/working_dir/aug_obj_12000/
# python -u -m scripts.train.train --obj_path=./data/working_dir/aug_obj/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=0 --pretrained_path=./data/working_dir/origin_model/backup/cross-hands_best.weights
python -u -m scripts.train.train --obj_path=./data/working_dir/aug_obj_12000/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1
