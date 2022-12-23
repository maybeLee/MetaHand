# This test script is used to evaluate the trained model and augmented model on the test set
std_list="0_5 1_0 2_0 4_0 8_0 16_0 32_0 64_0 128_0"
for std in $std_list
do
  echo "Current Gaussian Noise Is: ${std}"
  obj_path="./data_egohands/working_dir/testing/BackgroundGaussianMutation/BackgroundGaussian${std}_0.3/data/obj.data"
  cfg_path="./cfg/egohands.cfg"
  weights_path="./data_egohands/working_dir/testing/BackgroundGaussianMutation/BackgroundGaussian${std}_0.3/data/backup/egohands_best.weights"
  gpu="0,1,2"
  python -u -m scripts.test.test --obj_path=$obj_path --cfg_path=$cfg_path --weights_path=$weights_path --gpu=$gpu
done
