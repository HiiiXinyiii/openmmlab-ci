import logging
import os
import requests
import pytest
import generate_dataset
import util


class TestTools():
    @classmethod
    def setup_class(cls):
        """
        1. download dataset
        2. convert the balloon dataset into coco format
        """
        generate_dataset.prepare_balloon_dataset()

    def test_train(self):
        tmp_config_file = util.gen_uniq_str()+"_config.py"
        os.system("cp config.py %s" % tmp_config_file)
        cmd = "cd %s && tools/train.py tmp_config_file" % pytest.CODE_BASE

    # def test_test(self):
    #     cmd = "tools/test.py config.py work_dirs/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon/latest.pth --eval bbox segm"