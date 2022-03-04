ARG MMCV="ubuntu_1804_py_37_cuda_102_cudnn_7_torch_190_release"
ARG MMCV_VERSION="v1.4.0"

FROM registry.sensetime.com/mmcv/${MMCV}:${MMCV_VERSION}
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"
ARG DEBIAN_FRONTEND=noninteractive
ARG TENSORRT_VERSION="8.0.3.4"
ARG PPL_VERSION="v0.6.1"
ENV TZ=Asia/Shanghai
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"

WORKDIR /opt/deps
# Install CUDA Patches
COPY cuda-repo-ubuntu1804-10-2-local_10.2.1-1_amd64.deb cuda-repo-ubuntu1804-10-2-local_10.2.1-1_amd64.deb
RUN dpkg -i cuda-repo-ubuntu1804-10-2-local_10.2.1-1_amd64.deb
COPY cuda-repo-ubuntu1804-10-2-local_10.2.2-1_amd64.deb cuda-repo-ubuntu1804-10-2-local_10.2.2-1_amd64.deb
RUN dpkg -i cuda-repo-ubuntu1804-10-2-local_10.2.2-1_amd64.deb

ADD TensorRT-${TENSORRT_VERSION} ./TensorRT-${TENSORRT_VERSION}
RUN cd TensorRT-${TENSORRT_VERSION} \
    && python -m pip install python/tensorrt-${TENSORRT_VERSION}-cp37-none-linux_x86_64.whl \
    && python -m pip install uff/uff-0.6.9-py2.py3-none-any.whl \
    && python -m pip install graphsurgeon/graphsurgeon-0.4.5-py2.py3-none-any.whl \
    && python -m pip install onnx_graphsurgeon/onnx_graphsurgeon-0.3.10-py2.py3-none-any.whl

RUN apt-get update && apt-get install -y wget \
    && apt-get remove -y cmake cmake-data \
    && wget -O cmake-3.22.0-linux-x86_64.tar.gz https://cmake.org/files/v3.22/cmake-3.22.0-linux-x86_64.tar.gz \
    && tar zxvf cmake-3.22.0-linux-x86_64.tar.gz \
    && cp -r cmake-3.22.0-linux-x86_64 /usr/local/share/cmake-3.22 \
    && ln -s /usr/local/share/cmake-3.22/bin/cmake /usr/local/bin \
    && cmake --version

RUN apt-get install -y --no-install-recommends libssl-dev libopencv-dev libspdlog-dev libpython3.7

RUN git clone --branch ${PPL_VERSION} https://github.com/openppl-public/ppl.cv.git \
    && cd ppl.cv \
    && ./build.sh cuda \
    && ls -l /opt/deps/ppl.cv/cuda-build

RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf *.tar.gz