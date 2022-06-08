cd ../
TRAIN_ID=./data/training_id.txt
IMGDIR=./data/ImageSet
LABELDIR=./data/Labels
WORKDIR=./data/working_dir/origin_model
GPU=0
CFGPATH=./cfg/cross-hands.cfg
OBJPATH=${WORKDIR}/obj.data
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR}
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU
