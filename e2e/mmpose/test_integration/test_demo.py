import os
import pytest
import subprocess
import logging


def get_command():
    """
    Function: get the command for demo

    """
    command = [
        # 2D Animal Pose Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/macaque/res50_macaque_256x192.py") + " "
        + "https://download.openmmlab.com/mmpose/animal/resnet/res50_macaque_256x192-98f1dd3a_20210407.pth" + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/macaque/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/macaque/test_macaque.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # 2D Animal Pose Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_full_frame_without_det.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/fly/res152_fly_192x192.py") + " "
        + "https://download.openmmlab.com/mmpose/animal/resnet/res152_fly_192x192-fcafbd5a_20210407.pth" + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # Using MMDetection to detect animals
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + "https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_2x_coco/faster_rcnn_r50_fpn_2x_coco_bbox_mAP-0.384_20200504_210434-a5d8aa15.pth" + " "
        + os.path.join(pytest.CODEB_PATH, "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/horse10/res50_horse10_256x256-split1.py") + " "
        + "https://download.openmmlab.com/mmpose/animal/resnet/res50_horse10_256x256_split1-3a3dc37e_20210405.pth" + " "
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
