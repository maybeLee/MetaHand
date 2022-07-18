cd ../../
TRAIN_ID=./data_company/training_id.txt
IMGDIR=./data_company/ImageSet
LABELDIR=./data_company/Labels
WORKDIR=./data_company/working_dir/origin_model
GPU=0,1,2
CFGPATH=./cfg/cross-hands.cfg
OBJPATH=${WORKDIR}/obj.data
python -u -m scripts.train.prepare_train_data --source_path=${TRAIN_ID} --img_dir=${IMGDIR} --label_dir=${LABELDIR} --target_dir=${WORKDIR}
python -u -m scripts.train.train --obj_path=${OBJPATH} --cfg_path=$CFGPATH --retrain=1 --gpu=$GPU
echo "Finish Training"
