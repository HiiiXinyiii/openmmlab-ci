_base_ = [
    '../../../../../configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'
]
data = dict(
    workers_per_gpu=0
)
