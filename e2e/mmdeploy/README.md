# __MMDeploy__

## __1. Integration Test__

### __1.1 run properly__

#### __1.1.1 test MMDetection converter__

- We test it by calling these modules with certain sets of parameters.
- We catch the failure when the returncode is not 0.

```mermaid
graph LR;
    MMdetection-->convert
    convert-->case1
    case1-->config=configs/mmdet/detection/detection_tensorrt_dynamic-320x320-1344x1344.py
    case1-->cb_config=configs/yolo/yolov3_d53_mstrain-608_273e_coco.py

```

