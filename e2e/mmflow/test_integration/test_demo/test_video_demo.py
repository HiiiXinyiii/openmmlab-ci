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
    params = [(os.path.join(pytest.CODEB_PATH, "configs/pwcnet/pwcnet_8x1_slong_flyingchairs_384x448.py"),
               utils.get_cpt(file_path="configs/pwcnet/pwcnet_8x1_slong_flyingchairs_384x448.py",
                             code_path=pytest.CODEB_PATH)),
              (os.path.join(pytest.CODEB_PATH, "configs/maskflownet/maskflownet_8x1_800k_flyingchairs_384x448.py"),
               utils.get_cpt(file_path="configs/maskflownet/maskflownet_8x1_800k_flyingchairs_384x448.py",
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

    file_path = os.path.join(pytest.CODEB_PATH, 'demo/video_demo.py')
    # the cmd to be executed
    cmd = "python" + " " + file_path + " " \
          + os.path.join(pytest.CODEB_PATH, "demo/demo.mp4") + " " \
          + cfg_cpt + " " \
          + "result.mp4"

    # execute the command
    logging.getLogger().info("START to pytest command: " + cmd)

    res = subprocess.run(cmd.split())
    assert res.returncode == 0, \
        f'Failed to run video_demo.py with {cmd}'

    logging.getLogger().info("FINISH pytest command: " + cmd)
