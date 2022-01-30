import os
import requests
import pytest
import mmcv


def prepare_balloon_dataset():
    version = "v2.1"
    file_name = "balloon_dataset.zip"
    try:
        file_url = "https://github.com/matterport/Mask_RCNN/releases/download/%s/%s" % (version, file_name)
        r = requests.get(file_url)
        with open(pytest.CODEB_PATH, 'wb') as f:
            f.write(r.content)
        os.system("cd %s && unzip %s" % (pytest.CODEB_PATH, file_name))
        for t in ["train", "val"]:
            ann_file = pytest.CODEB_PATH+"/balloon/%s/annotation_coco.json" % t
            out_file = pytest.CODEB_PATH+"/balloon/%s/annotation_coco.json" % t
            image_prefix = pytest.CODEB_PATH+"/balloon/%s" % t
            convert_balloon_to_coco(ann_file, out_file, image_prefix)
        return True
    except Exception as e:
        pytest.getLogger().error("Get or convert bolloon dataset failed.")
        return False


def convert_balloon_to_coco(ann_file, out_file, image_prefix):
    data_infos = mmcv.load(ann_file)

    annotations = []
    images = []
    obj_count = 0
    for idx, v in enumerate(mmcv.track_iter_progress(data_infos.values())):
        filename = v['filename']
        img_path = os.path.join(image_prefix, filename)
        height, width = mmcv.imread(img_path).shape[:2]

        images.append(dict(
            id=idx,
            file_name=filename,
            height=height,
            width=width))

        bboxes = []
        labels = []
        masks = []
        for _, obj in v['regions'].items():
            assert not obj['region_attributes']
            obj = obj['shape_attributes']
            px = obj['all_points_x']
            py = obj['all_points_y']
            poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]

            x_min, y_min, x_max, y_max = (
                min(px), min(py), max(px), max(py))
            data_anno = dict(
                image_id=idx,
                id=obj_count,
                category_id=0,
                bbox=[x_min, y_min, x_max - x_min, y_max - y_min],
                area=(x_max - x_min) * (y_max - y_min),
                segmentation=[poly],
                iscrowd=0)
            annotations.append(data_anno)
            obj_count += 1

    coco_format_json = dict(
        images=images,
        annotations=annotations,
        categories=[{'id':0, 'name': 'balloon'}])
    mmcv.dump(coco_format_json, out_file)