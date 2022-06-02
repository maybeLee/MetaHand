cd ../
MutateName=B_random_erase_05
MutateType=RandomEraseMutation
python -u -m scripts.evaluation.evaluate -mi=./data/${MutateType}/$MutateName --threshold=0.3
base_dir=./data/working_dir/${MutateType}/${MutateName}_th03/
mkdir -p $base_dir
mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt
python -u -m scripts.train.prepare_train_data --source_path=${base_dir}/${MutateName}_violations.txt \
--img_dir=./data/${MutateType}/$MutateName --label_dir=./data/${MutateType}/label --target_dir=$base_dir/data/
python -u -m scripts.train.train --obj_path=${base_dir}/data/obj.data --cfg_path=./cfg/cross-hands.cfg --retrain=1
