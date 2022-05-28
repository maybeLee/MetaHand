MutateName=RandomNoiseB
python -u -m scripts.evaluation.evaluate -mi=./data/RandomNoiseMutation/$MutateName --threshold=0.05
mkdir -p ./data/working_dir/RandomNoiseMutation/${MutateName}_th08/
mv ${MutateName}_violations.txt ./data/working_dir/RandomNoiseMutation/${MutateName}_th08/${MutateName}_violations.txt
python -u -m scripts.train.prepare_train_data --source_path=./data/working_dir/RandomNoiseMutation/${MutateName}_th08/${MutateName}_violations.txt --img_dir=./data/RandomNoiseMutation/$MutateName --label_dir=./data/RandomNoiseMutation/label --target_dir=./data/working_dir/RandomNoiseMutation/${MutateName}_th08/data/
# python -u -m scripts.train.train --obj_path=./data/working_dir/aug_obj/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=0 --pretrained_path=./data/working_dir/origin_model/backup/cross-hands_best.weights
python -u -m scripts.train.train --obj_path=./data/working_dir/RandomNoiseMutation/${MutateName}_th08/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1
