ARG PYTORCH="1.6.0"
ARG CUDA="10.1"
ARG CUDNN="7"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0+PTX"
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
ENV FORCE_CUDA="1"
# ENV MMCV_CUDA_ARGS="-gencode=arch=compute_61,code=sm_61"
# ENV MMCV_WITH_OPS=1

# ARG TORCH="1.6.0+cu101"
# ARG TORCHVERSION="0.7.0+cu101"
# ARG PYTHON="3.7"
ARG DEBIAN_FRONTEND=noninteractive

# Using python3.7 in base image(pytorch)
# RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common ffmpeg libturbojpeg ninja-build libprotobuf-dev protobuf-compiler cmake git curl wget
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN if [ "$PYTHON" != "3.9" ] ; then apt-get install -y python${PYTHON}-dev python3-pip ; else apt-get install -y python${PYTHON} python3-pip python${PYTHON}-dev python${PYTHON}-distutils ; fi
# RUN apt-get clean && apt-get remove --purge -y \
#     && rm -rf /var/lib/apt/lists/*
# RUN unlink /usr/bin/python3 && python${PYTHON} -m pip install --upgrade pip && rm -f /usr/bin/pip3

RUN apt-get update && apt-get install -y ffmpeg libturbojpeg ninja-build libprotobuf-dev protobuf-compiler cmake git wget libpython3.7

# RUN python -c "import torch; print(torch.cuda.is_available())"
# RUN python -m pip install torch==${TORCH} torchvision==${TORCHVERSION} -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install psutil protobuf Pillow==6.2.2

# Install petrel oss sdk and petrel config file, make sure petrel-oss-python-sdk & openmmlab-ci exists
COPY petrel-oss-python-sdk /tmp
WORKDIR /tmp
RUN python setup.py develop
ADD openmmlab-ci/Dockerfiles/petreloss.conf /root/
RUN rm -rf petrel-oss-python-sdk

WORKDIR /opt/mmcv
COPY . /opt/mmcv

RUN MCV_WITH_ORT=1 MMCV_WITH_OPS=1 python -m pip install --no-cache-dir -e . && python .dev_scripts/check_installation.py