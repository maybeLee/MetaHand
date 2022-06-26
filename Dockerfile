FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-devel

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys A4B469963BF863CC
RUN apt-get update && apt-get install -y sudo pkg-config vim ffmpeg libsm6 libxext6 unzip wget git && pip install cmake

WORKDIR /root

