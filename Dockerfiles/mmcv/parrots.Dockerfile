ARG PARROTS_VERSION="pat_latest"

FROM registry.sensetime.com/parrots/parrots:${PARROTS_VERSION}
ARG DEBIAN_FRONTEND=noninteractive
ARG HTTP_PROXY="http://proxy.sensetime.com:3128"
ARG CONDA_ENV="pat20220303"
ENV TZ=Asia/Shanghai
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"
# ARG PYTORCH="1.6.0"
# ARG TORCHVISION="0.7.0"
# ARG PYTHON="3.7"
# ARG MMCV_VERSION="1.4.0"
ENV MMCV_WITH_OPS=1

RUN yum update -y && yum install -y turbojpeg
# RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common ffmpeg libturbojpeg ninja-build libprotobuf-dev protobuf-compiler cmake git curl wget
# RUN add-apt-repository ppa:deadsnakes/ppa
# # RUN if [ "$PYTHON" != "3.9" ] ; then apt-get install -y python${PYTHON}-dev python3-pip ; else apt-get install -y python${PYTHON} python3-pip python${PYTHON}-dev python${PYTHON}-distutils ; fi
# RUN apt-get clean && apt-get remove --purge -y \
#     && rm -rf /var/lib/apt/lists/*
# RUN unlink /usr/bin/python3 && python${PYTHON} -m pip install --upgrade pip && rm -f /usr/bin/pip3
# # Register the version in alternatives 
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON} 1 
# # Set python 3 as the default python 
# RUN update-alternatives --set python /usr/bin/python${PYTHON}
# RUN python -m pip install cython psutil protobuf Pillow==6.2.2
# RUN python -m pip install torch==${PYTORCH}+cpu torchvision==${TORCHVISION} -f https://download.pytorch.org/whl/torch_stable.html

# Install petrel oss sdk and petrel config file, make sure petrel-oss-python-sdk & openmmlab-ci exists
# COPY petrel-oss-python-sdk /tmp
# WORKDIR /tmp
# RUN python setup.py develop
# ADD openmmlab-ci/Dockerfiles/petreloss.conf /root/
# RUN rm -rf petrel-oss-python-sdk

WORKDIR /opt/mmcv
COPY . /opt/mmcv

# RUN python setup.py develop \
#     && python -m pip install --no-cache-dir -e .
# RUN python -m pip install install mmcv-full==${MMCV_VERSION} -f https://download.openmmlab.com/mmcv/dist/cpu/torch${PYTORCH}/index.html

RUN source ${CONDA_ENV} \
    && python setup.py build_ext -i \
    && pip install -r requirements/test.txt \
    && python .dev_scripts/check_installation.py

# RUN python setup.py check -m -s \
#     && python -m pip install --no-cache-dir -e . \
#     && python .dev_scripts/check_installation.py