import os
import pytest
import subprocess
import logging
import yaml
from ....utils import utils


def get_command():
    command = [
        # *********************************** 2d_human_pose_demo.md ***********************************
        # !!!!!!!! Not Complete !!!!!!!!!!!!!
        # 2D Human Pose Top-Down Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py") + " "
        + str(utils.get_cpt(
            file_path="configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py",
            code_path=pytest.CODEB_PATH)) + " "       # code_path=utils.MMPOSE_CB
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/test_coco.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_2d_human_pose_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")
