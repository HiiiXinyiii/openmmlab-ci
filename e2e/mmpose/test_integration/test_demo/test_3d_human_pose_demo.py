import os
import pytest
import subprocess
import logging
import yaml
from ....utils import utils


def get_command():
    # get meta.yaml which includes the checkpoints resources
    with open("test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # *********************************** 3d_human_pose_demo.md ***********************************
        # 3D Human Pose Two-stage Estimation Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/body3d_two_stage_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/body/3d_kpt_sview_rgb_img/pose_lift/h36m/simplebaseline3d_h36m.py") + " "
        + str(utils.get_cpt(
            file_path="configs/body/3d_kpt_sview_rgb_img/pose_lift/h36m/simplebaseline3d_h36m.py",
            code_path=pytest.CODEB_PATH)) + " "        # code_path=utils.MMPOSE_CB
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/h36m/h36m_coco.json") + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/h36m") + " "
        + "--camera-param-file " + os.path.join(pytest.CODEB_PATH, "tests/data/h36m/cameras.pkl") + " "
        + "--only-second-stage" + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results") + " "
        + "--rebase-keypoint-height" + " "
        + "--show-ground-truth",
        # 3D Human Pose Two-stage Estimation Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/body3d_two_stage_video_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['3d_human_pose_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py") + " "
        + str(utils.get_cpt(
            file_path="configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py",
            code_path=pytest.CODEB_PATH)) + " "        # code_path=utils.MMPOSE_CB
        + os.path.join(pytest.CODEB_PATH,
                       "configs/body/3d_kpt_sview_rgb_vid/video_pose_lift/h36m/videopose3d_h36m_243frames_fullconv_supervised_cpn_ft.py") + " "
        + str(utils.get_cpt(
            file_path="configs/body/3d_kpt_sview_rgb_vid/video_pose_lift/h36m/videopose3d_h36m_243frames_fullconv_supervised_cpn_ft.py",
            code_path=pytest.CODEB_PATH)) + " "        # code_path=utils.MMPOSE_CB
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results") + " "
        + "--rebase-keypoint-height"
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_3d_human_pose_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")
