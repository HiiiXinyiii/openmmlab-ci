import os
import pytest
import subprocess
import logging
import yaml
from ..prep_env import *
from ....utils import utils


def get_command():
    """
    Function: command from 2d_face_demo.md

    """
    command = [
        # ************************************** 2d_face_demo.md **************************************
        # 2D Face Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py") + " "
        + str(utils.get_cpt(
            file_path="configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/aflw/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/aflw/test_aflw.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_2d_face_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")


# *********************************************************************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************


def get_command_1():
    with open("./test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # ************************************** 2d_face_demo.md **************************************
        # 2D Face Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/face_video_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py") + " "
        + str(utils.get_cpt(
            file_path="configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--video-path " + str(resources['test_demo']['2d_face_demo']['videos'][0]['url']) + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
    ]

    return command


@pytest.mark.level(1)
@pytest.mark.parametrize('cmd', get_command_1())
def test_2d_face_demo_1(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")