rm -rf tools/opencv*
cd tools
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.x opencv
mv opencv_contrib-4.x opencv_contrib
sudo apt-get update
sudo apt-get upgrade
sudo apt install -y cmake g++ wget unzip
sudo apt-get install -y build-essential cmake unzip pkg-config
sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install -y libv4l-dev libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
cd opencv
# Create build directory
mkdir -p build && cd build
# Configure
export python_exec=`which python`
export include_dir=`python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())"`
export library=`python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))"`
export default_exec=`which python`
export site_package_path=`python -c "import site; print(site.getsitepackages()[0])"`

cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D OPENCV_ENABLE_NONFREE=OFF \
-D WITH_CUDA=ON \
-D WITH_CUDNN=ON \
-D OPENCV_DNN_CUDA=ON \
-D ENABLE_FAST_MATH=1 \
-D CUDA_FAST_MATH=1 \
-D CUDA_ARCH_BIN=7.5 \
-D WITH_CUBLAS=1 \
-D OPENCV_EXTRA_MODULES_PATH=~/tools/opencv_contrib/modules \
-D OPENCV_PYTHON3_INSTALL_PATH=$site_package_path \
-D HAVE_opencv_python3=ON \
-D PYTHON_INCLUDE_DIR=$include_dir \
-D PYTHON3_LIBRARY="${library}/libpython3.7m.so" \
-D PYTHON3_PACKAGES_PATH=$site_package_path \
-D PYTHON_EXECUTABLE=$python_exec \
-D BUILD_EXAMPLES=ON ..

# Build
make -j28

ln -s /root/tools/opencv/build/lib/python3/cv2.cpython-37m-x86_64-linux-gnu.so /opt/conda/lib/python3.7/site-packages/cv2.so
