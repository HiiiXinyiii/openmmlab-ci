import os
import pytest
import subprocess
import logging
import yaml
from ....utils import utils


def get_command():
    # get meta.yaml which includes the checkpoints resources
    with open("./test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # *********************************** 3d_hand_demo.md ***********************************
        "python " + os.path.join(pytest.CODEB_PATH, "demo/interhand3d_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/hand/3d_kpt_sview_rgb_img/internet/interhand3d/res50_interhand3d_all_256x256.py") + " "
        + str(utils.get_cpt(
            file_path="configs/hand/3d_kpt_sview_rgb_img/internet/interhand3d/res50_interhand3d_all_256x256.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH,
                                        "tests/data/interhand2.6m/test_interhand2.6m_data.json") + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/interhand2.6m") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results") + " "
        + "--rebase-keypoint-height",
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_3d_hand_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")
