ARG MMCV="ubuntu_1804_py_37_cuda_101_cudnn_7_torch_160"
ARG MMCV_VERSION="v1.3.16"

FROM ${MMCV}:${MMCV_VERSION}
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"

ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"

# RUN apt-get clean && apt-get remove --purge -y \
#     && rm -rf /var/lib/apt/lists/*

RUN python -m pip install libglib2.0-0 libsm6 libxrender-dev libxext6 \
    && python -m pip install git+https://github.com/votchallenge/toolkit.git \
    && python -m pip install attributee==0.1.5

WORKDIR /opt/mmtracking
COPY . /opt/mmtracking

RUN python -m pip install -r requirements.txt && python setup.py check -m -s && python -m pip install .