import logging
import os
import requests
import pytest


class TestTools():
    def setup():
        """
        1. download dataset
        2. convert the balloon dataset into coco format
        """
        pass

    def test_train(self):
        cmd = "tools/train.py configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon.py"

    def test_test(self):
        cmd = "tools/test.py configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon.py work_dirs/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon/latest.pth --eval bbox segm"