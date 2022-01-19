ARG MMCV="ubuntu_1804_py_37_torch_160_release"
ARG MMCV_VERSION="v1.4.0"

FROM ${MMCV}:${MMCV_VERSION}
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"
ARG ONNX_VERSION="1.8.1"

ENV TZ=Asia/Shanghai
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"
ENV ONNXRUNTIME_DIR=/opt/onnxruntime-linux-x64-${ONNX_VERSION}

RUN apt-get update && apt-get install -y libssl-dev libpython${PYTHON} wget \
    && apt-get remove -y cmake cmake-data \
    && wget -O cmake-3.22.0-linux-x86_64.tar.gz https://cmake.org/files/v3.22/cmake-3.22.0-linux-x86_64.tar.gz \
    && tar zxvf cmake-3.22.0-linux-x86_64.tar.gz \
    && cp -r cmake-3.22.0-linux-x86_64 /usr/local/share/cmake-3.22 \
    && ln -s /usr/local/share/cmake-3.22/bin/cmake /usr/local/bin \
    && cmake --version
RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install onnxruntime==${ONNX_VERSION}
WORKDIR /opt
RUN wget https://github.com/microsoft/onnxruntime/releases/download/v${ONNX_VERSION}/onnxruntime-linux-x64-${ONNX_VERSION}.tgz \
    tar -zxvf onnxruntime-linux-x64-${ONNX_VERSION}.tgz \
    rm -rf onnxruntime-linux-x64-${ONNX_VERSION}.tgz

WORKDIR /opt/mmdeploy
COPY . /opt/mmdeploy

RUN git submodule update --init --recursive
RUN pip install -r requirements.txt && pip install -e .
RUN mkdir build && cd build \
    && cmake .. \
    -DMMDEPLOY_BUILD_SDK=ON \
    -DCMAKE_CXX_COMPILER=g++-7 \
    -DONNXRUNTIME_DIR=${ONNXRUNTIME_DIR} \
    -DMMDEPLOY_TARGET_DEVICES="cpu" \
    -DMMDEPLOY_TARGET_BACKENDS=${BACKEND} \
    -DMMDEPLOY_CODEBASES=all \
    -DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \
    && cmake --build . -- -j4 && cmake --install .
RUN python tools/check_env.py