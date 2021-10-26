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
ARG PYTHON="3.7"

RUN apt-get update && apt-get install -y ffmpeg libturbojpeg ninja-build libprotobuf-dev protobuf-compiler cmake git

RUN if [ "$PYTHON" != "3.9" ] ; then apt-get install -y python${PYTHON}-dev ; fi

RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/*

# RUN python -m pip install torch==${TORCH} torchvision==${TORCHVERSION} -f https://download.pytorch.org/whl/torch_stable.html
RUN python -m pip install psutil protobuf Pillow==6.2.2

# Install petrel oss sdk and petrel config file
COPY /mnt/data1/jenkins/petrel-oss-python-sdk .
WORKDIR /tmp/petrel-oss-python-sdk
RUN python setup.py develop \
    && rm -rf /tmp/petrel-oss-python-sdk
ADD /mnt/data1/jenkins/petreloss.conf /

WORKDIR /opt/mmcv
COPY . /opt/mmcv

RUN MCV_WITH_ORT=1 MMCV_WITH_OPS=1 python -m pip install --no-cache-dir -e .