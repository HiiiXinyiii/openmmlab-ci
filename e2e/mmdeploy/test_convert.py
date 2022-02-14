import os
import logging
import pytest
import util

MMDET_PATH = util.CODEBASE_PATH+util.MMDET_CB+"/"


class TestConvertors():
    @pytest.mark.parametrize("config_cpt", [
        ('configs/mmdet/detection/detection_tensorrt_dynamic-320x320-1344x1344.py', 'configs/yolo/yolov3_d53_mstrain-608_273e_coco.py'),
    ])
    def test_det_convert(self, mmdet, config_cpt, ):
        cb_name, cb_branch = mmdet
        (config_path, cb_config_path) = config_cpt
        # get config and checkpoint file
        # cb_config_file = util.get_gitfile(cb_config_path, cb_name, cb_branch)
        # if not cb_config_file:
        #     pytest.fail("Get git config file failed.")
        # image_path = util.get_gitfile("demo/demo.jpg", cb_name, cb_branch)
        image_path = MMDET_PATH+"demo/demo.jpg"
        cb_cpt_path = util.get_cpt(cb_config_path, MMDET_PATH, cb_branch)
        device_str = "cuda:0"
        cmd = "tools/deploy.py %s %s %s %s --work-dir %s --show --device %s" % (
            config_path, 
            MMDET_PATH+"/"+cb_config_path, 
            os.path.realpath(cb_cpt_path), 
            image_path, 
            os.path.basename(os.path.realpath(cb_cpt_path)), 
            device_str)
        # execute cmd
        ret_code, ret_msg = util.python_exec(cmd)
        logging.info(ret_msg)
        assert ret_code