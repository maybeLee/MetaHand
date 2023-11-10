#!/bin/bash
# cd ../../
MutateType=ObjectGaussianMutation
DATASET=yolov7
GPU=0,1,2
data_dir=tools/yolov7/coco
log_dir=logs/yolov7/${MutateType}
weights_path=./tools/yolov7/runs/train/yolov7/weights/epoch_199.pt
output_dir=./tools/yolov7/runs/detect
mkdir -p $log_dir
mkdir -p $output_dir
th=0.3
# std_list="1_0 2_0 4_0 8_0 16_0 32_0 64_0 128_0"
ratio_list="01 02 03 04 05 06 07 08 09"
# for std in $std_list
for ratio in $ratio_list
do
    MutateName=object_gaussian_160_fixMutRatio_centerXY_${ratio}
    MR=2
    LABELDIR=same
    echo "Preparing Data For ${MutateName}"
    IMGDIR=./${data_dir}/${MutateType}/${MutateName}
    python -u -m scripts.evaluation.evaluate \
    -oi=./${data_dir}/images \
    -mi=${IMGDIR} \
    -ol=./${data_dir}/labels \
    -olf='yolov7' \
    -w=${weights_path} \
    -od=${output_dir} \
    --dataset=${DATASET} \
    --mr=${MR} \
    -img_size=320 \
    --jobs=12 \
    --threshold=${th} > ${log_dir}/${MutateName}_${th}.log

    base_dir=./tools/yolov7/runs/train/${MutateType}/${MutateName}_${th}
    v7_base=./runs/train/${MutateType}/${MutateName}_${th}
    mkdir -p $base_dir
    mv ${MutateName}_violations.txt ${base_dir}/${MutateName}_violations.txt

    # # new train file will be saved in ./{base_dir}/train.txt
    # python -u -m scripts.train.prepare_train_data \
    # --source_path=${base_dir}/${MutateName}_violations.txt \
    # --target_dir=${base_dir} \
    # --dataset=${DATASET}

    # train_txt=${v7_base}/train.txt
    # cp ./tools/yolov7/data/coco.yaml ${base_dir}/coco.yaml
    # # This line should use \" instead of \'
    # sed -i "s|train: .\/coco\/train2017.txt  # 118287 images|train: ${train_txt}|" ${base_dir}/coco.yaml

    # gpu_id=0,1,2
    # cd tools/yolov7
    # python -m torch.distributed.launch --nproc_per_node 3 \
    # --master_port 9527 train.py \
    # --workers 8 \
    # --device ${gpu_id} --sync-bn \
    # --batch-size 66 \
    # --data ${v7_base}/coco.yaml \
    # --img 320 320 --cfg cfg/training/yolov7.yaml \
    # --weights '' \
    # --name yolov7_${MutateName} \
    # --hyp data/hyp.scratch.p5.yaml
    # cd ../../
done

echo $"Finish All Jobs"

