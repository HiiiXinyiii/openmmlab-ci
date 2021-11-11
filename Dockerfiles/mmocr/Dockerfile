ARG MMDET="ubuntu_1804_py_37_cuda_101_cudnn_7_torch_160"
ARG MMCV_VERSION="v1.3.16"
ARG MMDET_VERSION="v2.18.0"

FROM ${MMDET}_mmcv_${MMCV_VERSION}:${MMDET_VERSION}
ARG HTTP_PROXY="http://172.16.1.135:3128"

ENV TORCH_CUDA_ARCH_LIST="7.0"
ENV HTTP_PROXY="$HTTP_PROXY"
ENV HTTPS_PROXY="$HTTP_PROXY"

# RUN apt-get clean && apt-get remove --purge -y \
#     && rm -rf /var/lib/apt/lists/*

# RUN python -m pip install pycocotools \
#     albumentations>=0.3.2 --no-binary imgaug,albumentations \
#     git+https://github.com/cocodataset/panopticapi.git

WORKDIR /opt/mmocr
COPY . /opt/mmocr

RUN python -m pip install -r requirements/tests.txt -r requirements/optional.txt && python setup.py check -m -s && python -m pip install .