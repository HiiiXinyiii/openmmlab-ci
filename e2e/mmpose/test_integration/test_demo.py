import os
import pytest
import subprocess
import logging
import yaml


def get_command():
    """
    Function: get the command for demo

    """
    # get meta.yaml which includes the checkpoints resources
    with open("./test_integration/meta.yaml", 'r') as f:
        data = yaml.safe_load(f)

    command = [
        # 2D Animal Pose Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/macaque/res50_macaque_256x192.py") + " "
        + str(data['test_demo']['2D_Animal_Pose_Image']['checkpoints'][0]['url']) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/macaque/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/macaque/test_macaque.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # 2D Animal Pose Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_full_frame_without_det.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/fly/res152_fly_192x192.py") + " "
        + str(data['test_demo']['2D_Animal_Pose_Video']['checkpoints'][0]['url']) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # Using MMDetection to detect animals
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(data['test_demo']['2D_Detect_Animal_Video']['checkpoints']['mmdet'][0]['url']) + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/horse10/res50_horse10_256x256-split1.py") + " "
        + str(data['test_demo']['2D_Detect_Animal_Video']['checkpoints']['mmpose'][0]['url']) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results") + " "
        + "--bbox-thr 0.1 "
        + "--kpt-thr 0.4 "
        + "--det-cat-id 18"
    ]

    return command


class TestDemo:
    """
    Function: test the demos in the MMPose
    """

    @pytest.mark.parametrize('cmd', get_command())
    def test_body3d(self, cmd):
        logging.getLogger().info(f"START pytest command: {cmd}")

        res = subprocess.run(cmd.split(' '))
        assert res.returncode == 0, \
            f'FAILED to run demo with command like {cmd}'

        logging.getLogger().info(f"FINISH pytest command: {cmd}")
