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
        # *********************************** 2d_pose_tracking_demo.md ***********************************
        # 2D Top-Down Video Human Pose Tracking Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_pose_tracking_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['2d_pose_tracking_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/res50_coco_256x192.py") + " "
        + str(utils.get_cpt(
            file_path="configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/res50_coco_256x192.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # 2D Top-Down Video Human Pose Tracking Demo with MMTracking
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_pose_tracking_demo_with_mmtracking.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmtracking_cfg/tracktor_faster-rcnn_r50_fpn_4e_mot17-private.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/res50_coco_256x192.py") + " "
        + str(utils.get_cpt(
            file_path="configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/res50_coco_256x192.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # 2D Bottom-Up Video Human Pose Tracking Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/bottom_up_pose_tracking_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/body/2d_kpt_sview_rgb_img/associative_embedding/coco/hrnet_w32_coco_512x512.py") + " "
        + str(utils.get_cpt(
            file_path="configs/body/2d_kpt_sview_rgb_img/associative_embedding/coco/hrnet_w32_coco_512x512.py",
            code_path=utils.MMPOSE_CB)) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_2d_pose_tracking_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")
