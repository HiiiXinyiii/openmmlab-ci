import logging
import os
import sys
import pytest
sys.path.append("..")
from utils import utils     # it may show error, but it will work since we have used sys.path.append

# for codebase
from mmcls.apis import inference_model, init_model, show_result_pyplot


def param_cfg_cpt():
    """
    Function: get the param that fits the directory structure

    """

    # (config and checkpoint)
    params = [(os.path.join(pytest.CODEB_PATH, "configs/resnet/resnet50_8xb32_in1k.py"),
               utils.get_cpt(file_path="configs/resnet/resnet50_8xb32_in1k.py",
                             code_path=pytest.CODEB_PATH)),
              (os.path.join(pytest.CODEB_PATH, "configs/deit/deit-base_pt-16xb64_in1k.py"),
               utils.get_cpt(file_path="configs/deit/deit-base_pt-16xb64_in1k.py",
                             code_path=pytest.CODEB_PATH))
              ]

    return params


@pytest.mark.parametrize('cfg_cpt', param_cfg_cpt())
def test_image_demo_without_displaying(cfg_cpt):
    config = cfg_cpt[0]
    checkpoint = cfg_cpt[1]
    device = "cuda:0"
    img = os.path.join(pytest.CODEB_PATH, 'demo/demo.JPEG')
    # build the model from a config file and a checkpoint file
    model = init_model(config, checkpoint, device)
    # test a single image
    result = inference_model(model, img)

    logging.getLogger().info(result)
