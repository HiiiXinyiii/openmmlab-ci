import logging
import os
import requests
import pytest
from mmdet.apis import init_detector, inference_detector


class TestExamples():
    def test_simple(self):
        config_file = os.path.join(pytest.CODEB_PATH, 'configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py')
        # download the checkpoint from model zoo and put it in `checkpoints/`
        checkpoint_file = "faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth"
        url = "https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/"+checkpoint_file
        if not os.path.exists(checkpoint_file):
            r = requests.get(url)
            print("Start downloading checkpoint file")
            open(checkpoint_file, 'wb').write(r.content)
        device = 'cuda:0'
        # init a detector
        model = init_detector(config_file, checkpoint_file, device=device)
        # inference the demo image
        logging.getLogger().info(inference_detector(model, os.path.join(pytest.CODEB_PATH, 'demo/demo.jpg')))