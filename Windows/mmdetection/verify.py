import os
import requests
from mmdet.apis import init_detector, inference_detector

config_file = 'configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'
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
print(inference_detector(model, 'demo/demo.jpg'))