ARG MMCV="ubuntu_1804_py_37_cuda_101_cudnn_7_torch_160"
ARG MMCV_VERSION="v1.3.16"

FROM ${MMCV}:${MMCV_VERSION}
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"
ARG DEBIAN_FRONTEND=noninteractive
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"

RUN apt update -y && apt install -y --no-install-recommends software-properties-common ffmpeg libglib2.0-0 libsndfile1 libsm6 libxrender-dev libxext6 \
    && python -m pip install librosa soundfile lmdb

RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/mmaction2
COPY . /opt/mmaction2

RUN python -m pip install -r requirements.txt && python setup.py check -m -s && python -m pip install .