# This test script is used to evaluate the trained model and augmented model on the test set
obj_path="./data_egohands/working_dir/BackgroundGaussianMutation/BackgroundGaussian16_0_0.3/data/obj.data"
cfg_path="./cfg/egohands.cfg"
weights_path="./data_egohands/working_dir/BackgroundGaussianMutation/BackgroundGaussian16_0_0.3/data/backup/egohands_final.weights"
gpu="0,1,2"
python -u -m scripts.test.test --obj_path=$obj_path --cfg_path=$cfg_path --weights_path=$weights_path --gpu=$gpu
