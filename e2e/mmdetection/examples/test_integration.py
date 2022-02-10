import logging
import requests
import pytest
import os
import json
import shutil
import random
import time


class coco_extract():
    def extract_json(self, read_json_path, write_json_path, size=200, chosen=None):
        """
        Function: extract a subset of the coco dataset

        :param chosen:
        :param size:
        :return:

        Note: parameter 'chosen' seems not to work
        """

        with open(read_json_path, 'r', encoding='utf-8') as fin:
            data_in = json.load(fin)

        # initialize the data_out
        data_out = {'info': data_in['info'],
                    'licenses': data_in['licenses'],
                    'images': [],
                    'annotations': [],
                    'categories': data_in['categories']}

        #######################
        # get its images attributes
        #######################
        images_num = len(data_in['images'])  # the quantity of the images of coco dataset
        images_id_picked = []  # the array of picked images' id
        # if the subset is chosen randomly
        if not chosen:
            random.seed(time.time())
            for i_image in range(size):
                while True:
                    i_image_picked = random.randint(0, images_num - 1)  # the random subscript of the image
                    i_image_id = data_in['images'][i_image_picked]['id']  # the id of this image
                    if i_image_id not in images_id_picked:
                        images_id_picked.append(i_image_id)
                        break
                # save this image into the output data
                data_out['images'].append(data_in['images'][i_image_picked])
        # if the subset is not chosen randomly
        else:
            if not isinstance(chosen, list):
                assert 'Type Error! The chosen images should be listed in List'
            images_id_picked = chosen
            for i_image in data_in['images']:
                data_out['images'].append(i_image)

        #######################
        # get its annotations attributes
        #######################
        for i_image_id in images_id_picked:
            for i_annotation in data_in['annotations']:
                if i_annotation['image_id'] == i_image_id:
                    data_out['annotations'].append(i_annotation)

        #######################
        # write as a new json file
        #######################
        with open(write_json_path, 'w', encoding='utf-8') as json_file:
            json_str = json.dumps(data_out, indent=4)
            json_file.write(json_str)

        return images_id_picked

    def extract_images(self, read_json_path, read_images_path, write_images_path, download=True):
        """
        Function: extract images

        :param read_json_path:
        :param read_images_path:
        :param write_images_path:
        :param download:
        :return:
        """

        with open(read_json_path, 'r', encoding='utf-8') as fin:
            data_in = json.load(fin)

        for i_image in data_in['images']:
            # if not download, we copy the corresponding images from local directory
            if not download:
                filepath = read_images_path + '/' + i_image['file_name']
                new_filepath = write_images_path + '/' + i_image['file_name']
                shutil.copy2(filepath, new_filepath)
            # if download == True, we download it from the internet
            else:
                r = requests.get(i_image['coco_url'])
                new_filepath = write_images_path + '/' + i_image['file_name']
                open(new_filepath, 'wb').write(r.content)


@pytest.fixture(scope='module')
def prep():
    """
    Function: prepare the json file and the recording images

    :return:
    """
    read_train_json_path = "data/coco/_annotations/instances_train2017.json"
    write_train_json_path = "data/coco/annotations/instances_train2017.json"
    read_val_json_path = "data/coco/_annotations/instances_val2017.json"
    write_val_json_path = "data/coco/annotations/instances_val2017.json"
    read_train_images_path = "data/coco/_train2017"
    write_train_images_path = "data/coco/train2017"
    read_val_images_path = "data/coco/_val2017"
    write_val_images_path = "data/coco/val2017"

    # extract part of train json
    if not os.path.exists(write_train_json_path):
        # delete the existing images which are extracted before
        if os.path.exists(write_train_images_path):
            shutil.rmtree(write_train_images_path)
        coco_extract().extract_json(read_json_path=read_train_json_path, write_json_path=write_train_json_path, chosen=None)
    print("准备好啦train.json")
    # extract part of train images
    if not os.path.exists(write_train_images_path):
        os.makedirs(write_train_images_path)
    if not os.listdir(write_train_images_path):
        coco_extract().extract_images(read_json_path=write_train_json_path, read_images_path=read_train_images_path, write_images_path=write_train_images_path)

    print("准备好了train")

    # extract part of val json
    if not os.path.exists(write_val_json_path):
        # delete the existing images which are extracted before
        if os.path.exists(write_val_images_path):
            shutil.rmtree(write_val_images_path)
        coco_extract().extract_json(read_json_path=read_val_json_path, write_json_path=write_val_json_path, chosen=None)
    print("完成val.json")
    # extract part of val images
    if not os.path.exists(write_val_images_path):       # if there isn't this directory, make a new one
        os.makedirs(write_val_images_path)
    if not os.listdir(write_val_images_path):   # if the directory is empty, it needs new image data
        coco_extract().extract_images(read_json_path=write_val_json_path, read_images_path=read_val_images_path, write_images_path=write_val_images_path)
    print("完成val image")


train_command = ['python -m tools.train configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py',
                 'python -m tools.train configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py',
                 'python -m tools.train configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py resume_from=faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth',
                 ]


class Test_integration:
    @pytest.mark.usefixtures('prep')
    @pytest.mark.parametrize('cmd', train_command)
    def test_train(self, cmd):
        """
        Function: test train.py

        :param cmd: the command user use to call train.py
        :return:
        """
        os.system(cmd)
        logging.getLogger().info("Finish pytest command: ", cmd)


if __name__ == '__main__':
    coco_extract().extract_images(read_json_path="data/coco/annotations/instances_train2017.json", read_images_path="data/coco/_train2017", write_images_path="data/coco/train2017", download=True)
