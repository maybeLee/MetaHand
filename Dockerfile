FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-devel

RUN apt-get update && apt-get install -y sudo pkg-config vim ffmpeg libsm6 libxext6 && pip install opencv-python

WORKDIR /root

