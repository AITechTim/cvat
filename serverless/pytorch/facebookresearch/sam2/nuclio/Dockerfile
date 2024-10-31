

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y install build-essential curl git python3 python3-pip ffmpeg libsm6 libxext6

# RUN SAM2_BUILD_CUDA=0 pip install git+https://github.com/facebookresearch/segment-anything-2.git@main
RUN SAM2_BUILD_CUDA=0 pip install git+https://github.com/facebookresearch/segment-anything-2.git@c2ec8e14a185632b0a5d8b161928ceb50197eddc



RUN curl -O https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_large.pt

RUN ln -s /usr/bin/pip3 /usr/local/bin/pip && ln -s /usr/bin/python3 /usr/bin/python
