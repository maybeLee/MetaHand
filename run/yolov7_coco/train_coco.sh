cd ../../tools/yolov7
BATCH_SIZE=66
DATA_PATH=data/coco.yaml
CFG_PATH=cfg/training/yolov7.yaml
IMG_SIZE=320
python -m torch.distributed.launch --nproc_per_node 3 --master_port 9527 train.py --workers 8 --device 0,1,2 \
--sync-bn --batch-size ${BATCH_SIZE} \
--data ${DATA_PATH} --img ${IMG_SIZE} ${IMG_SIZE} \
--cfg ${CFG_PATH} --weights '' \
--name yolov7 --hyp data/hyp.scratch.p5.yaml
