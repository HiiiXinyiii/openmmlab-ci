import os
import pytest
import logging
import subprocess
import sys
sys.path.append("..")
from utils import utils     # it may show error, but it will work since we have used sys.path.append


def param_cfg_cpt():
    """
    Function: get the param that fits the directory structure

    """

    # (config and checkpoint)
    params = [(os.path.join(pytest.CODEB_PATH, "configs/resnet/resnet50_8xb32_in1k.py"),
               utils.get_cpt(file_path="configs/resnet/resnet50_8xb32_in1k.py",
                             code_path=pytest.CODEB_PATH))
              ]

    res = []
    for i_param in params:
        tmp = ""
        for j_part in i_param:
            tmp = tmp + str(j_part) + " "

        res.append(tmp.strip())

    return res


@pytest.mark.parametrize('cfg_cpt', param_cfg_cpt())
def test_image_demo(cfg_cpt):
    """
    Function: test test.py

    :param cmd_param: the command user use to call test.py
    :return:
    """

    file_path = os.path.join(pytest.CODEB_PATH, 'demo/image_demo.py')
    # the cmd to be executed
    cmd = "python" + " " + file_path + " " + \
          os.path.join(pytest.CODEB_PATH, "demo/bird.JPEG") + " " + cfg_cpt
    # execute the command
    logging.getLogger().info("START to pytest command: " + cmd)

    res = subprocess.run(cmd.split())
    assert res.returncode == 0, \
        f'Failed to run train.py with {cmd}'

    logging.getLogger().info("FINISH pytest command: " + cmd)
