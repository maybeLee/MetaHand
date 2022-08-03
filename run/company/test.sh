# This test script is used to evaluate the trained model and augmented model on the test set
# working_dir="./data_company/working_dir/BackgroundGaussianMutation/B_guassian_160_fixMutRatio_centerXY_03_th03/data"
working_dir="./data_company/working_dir/origin_model"
obj_path="${working_dir}/obj.data"
cfg_path="./cfg/cross-hands.cfg"
weights_path="${working_dir}/backup/cross-hands_best.weights"
gpu="0,1,2"
python -u -m scripts.test.test --obj_path=$obj_path --cfg_path=$cfg_path --weights_path=$weights_path --gpu=$gpu

