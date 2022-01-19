ARG IMAGE="ubuntu_1804_py_37_torch_160"
ARG BACKEND="ort"
ARG TAG="v1"

FROM registry.sensetime.com/mmdeploy/${IMAGE}_${BACKEND}:${TAG}
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"
ARG ONNX_VERSION="1.8.1"
ARG BACKEND

ENV TZ=Asia/Shanghai
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"
ENV ONNXRUNTIME_DIR=/opt/onnxruntime-linux-x64-${ONNX_VERSION}

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
RUN python3 tools/check_env.py