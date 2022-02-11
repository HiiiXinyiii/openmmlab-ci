import pytest
import util


class TestConvertors():
    @pytest.mark.parametrize("config_cpt", [
        (pytest.CODE_PATH+'/configs/mmdet/detection/detection_tensorrt_dynamic-320x320-1344x1344.py', 'configs/yolo/yolov3_d53_mstrain-608_273e_coco.py'),
    ])
    def test_det_convert(self, mmdet, config_cpt):
        cb_name, cb_branch = mmdet
        (config_path, cb_config_path) = config_cpt
        # get config and checkpoint file
        if not util.get_gitfile(cb_config_path, cb_name, cb_branch):
            pytest.fail("Get git config file failed.")
        image_path = util.get_gitfile("demo/demo.jpg", cb_name, cb_branch)
        cb_cpt_path = util.get_cpt(cb_config_path, cb_name, cb_branch)
        device_str = "cuda:0"
        cmd = "tools/deploy.py %s %s %s %s --work-dir . --show --device %s" % (config_path, cb_config_path, cb_cpt_path, image_path, device_str)
        # execute cmd
        ret = util.python_exec(cmd)
        if ret["returncode"] != 0:
            assert False
        pytest.getLogger().debug(ret["stdout"])
        assert True