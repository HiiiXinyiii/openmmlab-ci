import pytest


class TestConvertors():
    @pytest.fixture()
    def config_cpt():
        return [
            ('configs/yolo/yolov3_d53_mstrain-608_273e_coco.py', 'yolo/yolov3_d53_mstrain-608_273e_coco.pth')
        ]

    def test_convert(self, config_cpt):
        config_name, cpt_name = config_cpt
        # get config and checkpoint file
        cb_config_path = ""
        cb_cpt_path = ""
        config_path = ""
        image_path = ""
        device_str = "cuda:0"
        cmd = "tools/deploy.py %s %s %s %s --work-dir . --show --device %s" % (config_path, cb_config_path, cb_cpt_path, image_path, device_str)
        # execute cmd
        

