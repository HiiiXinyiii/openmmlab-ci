import os
import pytest
import subprocess
import logging
import yaml
from ..prep_env import *
from ....utils import utils


def get_command():
    # get meta.yaml which includes the checkpoints resources
    with open("./test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # *********************************** 2d_wholebody_pose_demo.md ***********************************
        # 2D Human Whole-Body Pose Top-Down Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py") + " "
        + str(utils.get_cpt(
            file_path="configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/test_coco.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # Using mmdet for human bounding box detection
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['2d_wholebody_pose_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py") + " "
        + str(utils.get_cpt(
            file_path="configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/") + " "
        + "--img " + "000000196141.jpg" + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # 2D Human Whole-Body Pose Top-Down Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['2d_wholebody_pose_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py") + " "
        + str(utils.get_cpt(
            file_path="configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--video-path " + str(resources['test_demo']['2d_wholebody_pose_demo']['videos'][0]['url']) + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_2d_wholebody_pose_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")
