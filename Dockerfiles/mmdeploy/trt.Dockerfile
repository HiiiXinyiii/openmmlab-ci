ARG MMCV="ubuntu_1804_py_39_cuda_111_cudnn_8_torch_190_release"
ARG MMCV_VERSION="v1.4.0"
ARG TENSORRT_VERSION="8.0.3.4"

FROM mmcv_${MMCV}:${MMCV_VERSION}
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"

ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"
ARG TENSORRT_VERSION="8.0.3.4"

WORKDIR /opt/deps
ADD /mnt/data1/jenkins/deps/TensorRT-${TENSORRT_VERSION}.Linux.x86_64-gnu.cuda-11.3.cudnn8.2.tar.gz .
RUN tar xzvf TensorRT-${TENSORRT_VERSION}.Linux.x86_64-gnu.cuda-11.3.cudnn8.2.tar.gz \
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/deps/TensorRT-${TENSORRT_VERSION}/lib \
    cd TensorRT-${TENSORRT_VERSION}/python \
    python -m pip install tensorrt-${TENSORRT_VERSION}-cp37-none-linux_x86_64.whl && cd .. \
    cd TensorRT-${TENSORRT_VERSION}/uff \
    python -m pip install uff-0.6.9-py2.py3-none-any.whl && cd .. \
    cd TensorRT-${TENSORRT_VERSION}/graphsurgeon \
    python -m pip install graphsurgeon-0.4.5-py2.py3-none-any.whl && cd ..\
    cd TensorRT-${TENSORRT_VERSION}/onnx_graphsurgeon \
    python -m pip install onnx_graphsurgeon-0.3.10-py2.py3-none-any.whl

RUN apt-get update && apt-get install -y wget 
RUN wget https://cmake.org/files/v3.22/cmake-3.22.0-linux-x86_64.tar.gz \
    tar -zxvf cmake-3.22.0-linux-x86_64.tar.gz \
    mv cmake-3.22.0-linux-x86_64 cmake-3.22.0 \
    ln -sf /cmake-3.12.2/bin/* /usr/bin

RUN apt-get install -y libssl-dev libopencv-dev libspdlog-dev

RUN git clone git@github.com:openppl-public/ppl.cv.git \
    cd ppl.cv \
    ./build.sh cuda

RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/mmdeploy
COPY . /opt/mmdeploy

RUN git submodule update --init --recursive
RUN pip install -e . all
RUN mkdir build && cd build \
    cmake .. \
   -DMMDEPLOY_BUILD_SDK=ON \
   -DCMAKE_CXX_COMPILER=g++-7 \
   -Dpplcv_DIR=/opt/deps/ppl.cv/install/lib/cmake/ppl \
   -DTENSORRT_DIR=/opt/deps/TensorRT-${TENSORRT_VERSION} \
#    -DCUDNN_DIR=/path/to/cudnn \
   -DMMDEPLOY_TARGET_DEVICES="cuda;cpu" \
   -DMMDEPLOY_TARGET_BACKENDS=trt \
   -DMMDEPLOY_CODEBASES=all \
    && cmake --build . -- -4 && cmake --install .

