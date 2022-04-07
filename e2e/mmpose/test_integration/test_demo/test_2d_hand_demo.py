import os
import pytest
import subprocess
import logging
import yaml
from ....utils import utils


def get_command():
    # get meta.yaml which includes the checkpoints and videos resources
    with open("test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # ************************************** 2d_hand_demo.md **************************************
        # 2D Hand Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/cascade_rcnn_x101_64x4d_fpn_1class.py") + " "
        + str(resources['test_demo']['2d_hand_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/onehand10k/res50_onehand10k_256x256.py") + " "
        + str(utils.get_cpt(
            file_path="configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/onehand10k/res50_onehand10k_256x256.py",
            code_path=pytest.CODEB_PATH)) + " "  # code_path=utils.MMPOSE_CB
        + "--video-path " + str(resources['test_demo']['2d_hand_demo']['videos'][0]['url']) + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_2d_hand_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")


# *********************************************************************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************


def get_command_1():
    # get meta.yaml which includes the checkpoints resources
    with open("./test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # *********************************** 2d_hand_demo.md ***********************************
        # 2D Hand Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/onehand10k/res50_onehand10k_256x256.py") + " "
        + str(utils.get_cpt(
            file_path="configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/onehand10k/res50_onehand10k_256x256.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/onehand10k/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/onehand10k/test_onehand10k.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results")
    ]

    return command


# @pytest.mark.level(1)
# @pytest.mark.parametrize('cmd', get_command_1())
# def test_2d_hand_demo_1(cmd):
#     logging.getLogger().info(f"START pytest command: {cmd}")
#
#     res = subprocess.run(cmd.split(' '))
#     assert res.returncode == 0, \
#         f'FAILED to run demo with command like {cmd}'
#
#     logging.getLogger().info(f"FINISH pytest command: {cmd}")
