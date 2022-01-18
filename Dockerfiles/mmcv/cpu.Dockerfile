ARG OS_VERSION="18.04"

FROM ubuntu:${OS_VERSION}}

ARG PYTORCH="1.6.0"
ARG TORCHVISION="0.7.0"
ARG PYTHON="3.7"
# ARG MMCV_VERSION="1.4.0"

RUN apt-get update && apt-get install -y ffmpeg libturbojpeg ninja-build libprotobuf-dev protobuf-compiler cmake git wget
RUN if [ "$PYTHON" != "3.9" ] ; then apt-get install -y python${PYTHON}-dev ; else fi
RUN apt-get install -y python${PYTHON} python3-pip
RUN apt-get clean && apt-get remove --purge -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install torch==${PYTORCH}+cpu torchvision==${TORCHVISION} -f https://download.pytorch.org/whl/torch_stable.html
RUN python -m pip install psutil protobuf Pillow==6.2.2

# Install petrel oss sdk and petrel config file, make sure petrel-oss-python-sdk & openmmlab-ci exists
COPY petrel-oss-python-sdk /tmp
WORKDIR /tmp
RUN python setup.py develop
ADD openmmlab-ci/Dockerfiles/petreloss.conf /root/
RUN rm -rf petrel-oss-python-sdk

# WORKDIR /opt/mmcv
# COPY . /opt/mmcv

RUN python -m pip install --no-cache-dir -e .
# RUN pip install mmcv-full==${MMCV_VERSION} -f https://download.openmmlab.com/mmcv/dist/cpu/torch${TORCH}/index.html