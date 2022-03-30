import os
import pytest
import subprocess
import logging
import yaml
from .prep_env import *


def get_command_level_2():
    with open("./test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # 2D Face Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/face_video_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py") + " "
        + str(resources['test_demo']['2d_face_demo']['checkpoints'][0]['url']) + " "
        + "--video-path " + str(resources['test_demo']['2d_face_demo']['videos'][0]['url']) + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # *********************************** 2d_hand_demo.md ***********************************
        # 2D Hand Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/onehand10k/res50_onehand10k_256x256.py") + " "
        + str(resources['test_demo']['2d_hand_demo']['checkpoints'][0]['url']) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/onehand10k/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/onehand10k/test_onehand10k.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results")
    ]

    return command


def get_command_level_0():
    """
    Function: get the command for demo

    """
    logging.getLogger().info("Finish Install All the Environment!! ")

    # get meta.yaml which includes the checkpoints resources
    with open("./test_integration/meta.yaml", 'r') as f:
        resources = yaml.safe_load(f)

    command = [
        # *************************************** 2d_animal_demo.md ***************************************
        # 2D Animal Pose Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/macaque/res50_macaque_256x192.py") + " "
        + str(resources['test_demo']['2d_animal_demo']['checkpoints'][0]['url']) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/macaque/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/macaque/test_macaque.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # 2D Animal Pose Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_full_frame_without_det.py") + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/fly/res152_fly_192x192.py") + " "
        + str(resources['test_demo']['2d_animal_demo']['checkpoints'][1]['url']) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # Using MMDetection to detect animals (2D_Detect_Animal_Video)
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['2d_animal_demo']['checkpoints'][2]['url']) + " "
        + os.path.join(pytest.CODEB_PATH,
                       "configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/horse10/res50_horse10_256x256-split1.py") + " "
        + str(resources['test_demo']['2d_animal_demo']['checkpoints'][3]['url']) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results") + " "
        + "--bbox-thr 0.1 "
        + "--kpt-thr 0.4 "
        + "--det-cat-id 18",

        # ************************************** 2d_face_demo.md **************************************
        # 2D Face Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py") + " "
        + str(resources['test_demo']['2d_face_demo']['checkpoints'][0]['url']) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/aflw/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH,  "tests/data/aflw/test_aflw.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # ************************************** 2d_hand_demo.md **************************************
        # 2D Hand Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/cascade_rcnn_x101_64x4d_fpn_1class.py") + " "
        + str(resources['test_demo']['2d_hand_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH, "configs/hand/2d_kpt_sview_rgb_img/topdown_heatmap/onehand10k/res50_onehand10k_256x256.py") + " "
        + str(resources['test_demo']['2d_hand_demo']['checkpoints'][0]['url']) + " "
        + "--video-path " + str(resources['test_demo']['2d_hand_demo']['videos'][0]['url']) + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # *********************************** 2d_human_pose_demo.md ***********************************
        # !!!!!!!! Not Complete !!!!!!!!!!!!!
        # 2D Human Pose Top-Down Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py") + " "
        + str(resources['test_demo']['2d_human_pose_demo']['checkpoints'][0]['url']) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/test_coco.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # *********************************** 2d_pose_tracking_demo.md ***********************************
        # 2D Top-Down Video Human Pose Tracking Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_pose_tracking_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['2d_pose_tracking_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH, "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/res50_coco_256x192.py") + " "
        + str(resources['test_demo']['2d_pose_tracking_demo']['checkpoints'][0]['url']) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # 2D Top-Down Video Human Pose Tracking Demo with MMTracking
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_pose_tracking_demo_with_mmtracking.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmtracking_cfg/tracktor_faster-rcnn_r50_fpn_4e_mot17-private.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/res50_coco_256x192.py") + " "
        + str(resources['test_demo']['2d_pose_tracking_demo']['checkpoints'][0]['url']) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # 2D Bottom-Up Video Human Pose Tracking Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/bottom_up_pose_tracking_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/body/2d_kpt_sview_rgb_img/associative_embedding/coco/hrnet_w32_coco_512x512.py") + " "
        + str(resources['test_demo']['2d_pose_tracking_demo']['checkpoints'][2]['url']) + " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # *********************************** 2d_wholebody_pose_demo.md ***********************************
        # 2D Human Whole-Body Pose Top-Down Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py") + " "
        + str(resources['test_demo']['2d_wholebody_pose_demo']['checkpoints'][0]['url']) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/") + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/test_coco.json") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # Using mmdet for human bounding box detection
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_img_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['2d_wholebody_pose_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH, "configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py") + " "
        + str(resources['test_demo']['2d_wholebody_pose_demo']['checkpoints'][0]['url']) + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/coco/") + " "
        + "--img " + "000000196141.jpg" + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
        # 2D Human Whole-Body Pose Top-Down Video Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/top_down_video_demo_with_mmdet.py") + " "
        + os.path.join(pytest.CODEB_PATH, "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py") + " "
        + str(resources['test_demo']['2d_wholebody_pose_demo']['checkpoints'][1]['url']) + " "
        + os.path.join(pytest.CODEB_PATH, "configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py") + " "
        + str(resources['test_demo']['2d_wholebody_pose_demo']['checkpoints'][0]['url']) + " "
        + "--video-path " + str(resources['test_demo']['2d_wholebody_pose_demo']['videos'][0]['url']) + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # *********************************** 3d_body_mesh_demo.md ***********************************
        "python " + os.path.join(pytest.CODEB_PATH, "demo/mesh_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/body/3d_mesh_sview_rgb_img/hmr/mixed/res50_mixed_224x224.py") + " "
        + str(resources['test_demo']['3d_body_mesh_demo']['checkpoints'][0]['url']) + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/h36m/h36m_coco.json") + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/h36m") + " "
        + "-out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),

        # *********************************** 3d_hand_demo.md ***********************************
        "python " + os.path.join(pytest.CODEB_PATH, "demo/interhand3d_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/hand/3d_kpt_sview_rgb_img/internet/interhand3d/res50_interhand3d_all_256x256.py") + " "
        + str(resources['test_demo']['3d_hand_demo']['checkpoints'][0]['url']) + " "
        + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/interhand2.6m/test_interhand2.6m_data.json") + " "
        + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/interhand2.6m") + " "
        + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results") + " "
        + "--rebase-keypoint-height",

        # *********************************** 3d_human_pose_demo.md ***********************************
        # 3D Human Pose Two-stage Estimation Image Demo
        "python " + os.path.join(pytest.CODEB_PATH, "demo/body3d_two_stage_img_demo.py") + " "
        + os.path.join(pytest.CODEB_PATH, "configs/body/3d_kpt_sview_rgb_img/pose_lift/h36m/simplebaseline3d_h36m.py") + " "
        + str(resources['test_demo']['3d_human_pose_demo']['checkpoints'][0]['url']) + " "
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
        + os.path.join(pytest.CODEB_PATH, "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py") + " "
        + str(resources['test_demo']['3d_human_pose_demo']['checkpoints'][2]['url']) + " "
        + os.path.join(pytest.CODEB_PATH, "configs/body/3d_kpt_sview_rgb_vid/video_pose_lift/h36m/videopose3d_h36m_243frames_fullconv_supervised_cpn_ft.py") + " "
        + str(resources['test_demo']['3d_human_pose_demo']['checkpoints'][3]['url'])+ " "
        + "--video-path " + os.path.join(pytest.CODEB_PATH, "demo/resources/demo.mp4") + " "
        + "--out-video-root " + os.path.join(pytest.CODEB_PATH, "vis_results") + " "
        + "--rebase-keypoint-height"
    ]

    return command


def get_command_all():
    return get_command_level_0() + get_command_level_2()


class TestDemo:
    """
    Function: test the demos in the MMPose
    """

    # test the cases which are the most important
    @pytest.mark.usefixtures('prep_env_for_level_0')
    @pytest.mark.parametrize('cmd', get_command_level_0())
    def test_demo_level_0(self, cmd):
        logging.getLogger().info(f"START pytest command: {cmd}")

        res = subprocess.run(cmd.split(' '))
        assert res.returncode == 0, \
            f'FAILED to run demo with command like {cmd}'

        logging.getLogger().info(f"FINISH pytest command: {cmd}")

    # # test the cases which are at level 2
    # @pytest.mark.usefixtures('prep_env_for_level_2')
    # @pytest.mark.parametrize('cmd', get_command_level_2())
    # # @pytest.mark.level(2)
    # def test_demo_level_1(self, cmd):
    #     logging.getLogger().info(f"START pytest command: {cmd}")
    #
    #     res = subprocess.run(cmd.split(' '))
    #     assert res.returncode == 0, \
    #         f'FAILED to run demo with command like {cmd}'
    #
    #     logging.getLogger().info(f"FINISH pytest command: {cmd}")
