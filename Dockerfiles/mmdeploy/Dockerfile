ARG MMDET="ubuntu_1804_py_37_cuda_101_cudnn_7_torch_160"
ARG MMCV_VERSION="v1.3.16"
ARG MMDET_VERSION="v2.18.0"

FROM ${MMDET}_mmcv_${MMCV_VERSION}:${MMDET_VERSION}
ARG HTTP_PROXY="http://172.16.1.135:3128"

ENV TORCH_CUDA_ARCH_LIST="7.0"
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"
ENV ONNXRUNTIME_DIR=/opt/onnxruntime-linux-x64-1.8.1

RUN apt-get update && apt-get install -y libssl-dev
RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install onnxruntime==1.8.1
WORKDIR /opt
RUN wget https://github.com/microsoft/onnxruntime/releases/download/v1.8.1/onnxruntime-linux-x64-1.8.1.tgz \
    tar -zxvf onnxruntime-linux-x64-1.8.1.tgz \
    cd onnxruntime-linux-x64-1.8.1 \
    export LD_LIBRARY_PATH=${ONNXRUNTIME_DIR}/lib:$LD_LIBRARY_PATH
    mkdir build && cd build \
    cmake -DBUILD_ONNXRUNTIME_OPS=ON -DONNXRUNTIME_DIR=${ONNXRUNTIME_DIR} .. \
    make -j8

WORKDIR /opt/deploy_prototype
COPY . /opt/deploy_prototype

RUN git submodule update --init --recursive
RUN python -m pip install -r requirements/tests.txt -r requirements/optional.txt && python setup.py check -m -s && python -m pip install .