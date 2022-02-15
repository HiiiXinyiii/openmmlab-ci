ARG MMCV="ubuntu_1804_py_37_cuda_101_cudnn_7_torch_160"
ARG MMCV_VERSION="v1.3.16"

FROM ${MMCV}:${MMCV_VERSION}
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"
ARG DEBIAN_FRONTEND=noninteractive
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"

RUN apt update -y && apt install -y --no-install-recommends software-properties-common libglib2.0-0 libsm6 libxrender-dev libxext6 libturbojpeg libprotobuf-dev protobuf-compiler \
    && python -m pip install protobuf

RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/mmpose
COPY . /opt/mmpose

RUN python -m pip install -r requirements.txt && python setup.py check -m -s && python -m pip install .