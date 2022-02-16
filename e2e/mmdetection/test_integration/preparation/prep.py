import requests
import json
import shutil
import random
import time
import re
import pytest
import os


# extract part of coco dataset
class CocoExtract:
    def extract_json(self, read_json_path, write_json_path, size=200, chosen=None):
        """
        Function: extract a subset of the coco dataset

        :param chosen:
        :param size:
        :return:

        Note: parameter 'chosen' seems not to work
        """
        try:
            with open(read_json_path, 'r', encoding='utf-8') as fin:
                data_in = json.load(fin)
        except FileNotFoundError:
            assert f'Fail to open file {read_json_path} when extracting json from coco dataset'

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
        filedir, filename = os.path.split(write_json_path)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        try:
            with open(write_json_path, 'w+', encoding='utf-8') as json_file:
                json_str = json.dumps(data_out, indent=4)
                json_file.write(json_str)
        except FileNotFoundError:
            assert f'Fail to open file {write_json_path}'

        return images_id_picked

    def extract_images(self, read_json_path, write_images_path, read_images_path=None, download=True):
        """
        Function: extract images

        :param read_json_path:
        :param read_images_path:
        :param write_images_path:
        :param download:
        :return:
        """
        try:
            with open(read_json_path, 'r', encoding='utf-8') as fin:
                data_in = json.load(fin)
        except FileNotFoundError:
            assert f'Fail to open file {read_json_path}'

        # if the write_images_path doesn't exist, then create one
        if not os.path.exists(write_images_path):
            os.makedirs(write_images_path)

        # copy or download the images
        for i_image in data_in['images']:
            # if not download, we copy the corresponding images from local directory
            if not download:
                filepath = os.path.join(read_images_path, i_image['file_name'])
                new_filepath = os.path.join(write_images_path, i_image['file_name'])
                shutil.copy2(filepath, new_filepath)
            # if download == True, we download it from the internet
            else:
                r = requests.get(i_image['coco_url'])
                new_filepath = os.path.join(write_images_path, i_image['file_name'])
                try:
                    with open(new_filepath, 'wb') as f:
                        f.write(r.content)
                except FileNotFoundError:
                    assert f'Fail to write images {new_filepath}'


# list all the config file path in the project
def get_all_config_path():
    """
    Function: list all the config file path in the project

    :return: the path of the all config files
    """
    config_path = []  # save the result

    config_lib_path = os.path.join(os.path.join(os.getcwd(), 'configs'))  # the path of the all config files
    for parent, dirnames, filenames in os.walk(config_lib_path):
        # skip __base__ directory, because we dont directly use it, it's the base of other configs
        if re.match(pattern=".*__base__.*", string=parent):
            continue
        # add all the file
        for i_filename in filenames:
            # We just use .py file, because in this directory we think all .py files are the same as config files
            if re.match(pattern=".*\\.py", string=i_filename):
                path = os.path.join(parent, i_filename)
                config_path.append(path)

    return config_path


@pytest.fixture(scope='module')
def prep():
    """
    Function: prepare before

    :return:
    """
    # On server we think the root path is '/opt/mmdetection/openmmlab-ci/e2e/mmdetection/'
    # In this way, we don't have to modify the original config file
    # Because in config, they use 'data/coco/annotations/instances_val2017.json' in default
    # But actually this download path is not what the author wants the users to use
    read_train_json_path = os.path.join(os.getcwd(), "data/coco_annotations/instances_train2017.json")
    write_train_json_path = os.path.join(os.getcwd(), "data/coco/annotations/instances_train2017.json")
    read_val_json_path = os.path.join(os.getcwd(), "data/coco_annotations/instances_val2017.json")
    write_val_json_path = os.path.join(os.getcwd(), "data/coco/annotations/instances_val2017.json")
    read_train_images_path = os.path.join(os.getcwd(), "data/coco/train2017")    # use when not download
    write_train_images_path = os.path.join(os.getcwd(), "data/coco/train2017")
    read_val_images_path = os.path.join(os.getcwd(), "data/coco/val2017")        # use when not download
    write_val_images_path = os.path.join(os.getcwd(), "data/coco/val2017")

    # extract part of train json
    if not os.path.exists(write_train_json_path):
        # delete the existing images which are extracted before
        if os.path.exists(write_train_images_path):
            shutil.rmtree(write_train_images_path)
        CocoExtract().extract_json(read_json_path=read_train_json_path, write_json_path=write_train_json_path,
                                   chosen=None)
    # extract part of train images
    if not os.path.exists(write_train_images_path):
        os.makedirs(write_train_images_path)
    if not os.listdir(write_train_images_path):
        CocoExtract().extract_images(read_json_path=write_train_json_path, read_images_path=read_train_images_path,
                                     write_images_path=write_train_images_path, download=True)

    # extract part of val json
    if not os.path.exists(write_val_json_path):
        # delete the existing images which are extracted before
        if os.path.exists(write_val_images_path):
            shutil.rmtree(write_val_images_path)
        CocoExtract().extract_json(read_json_path=read_val_json_path, write_json_path=write_val_json_path, chosen=None)
    # extract part of val images
    if not os.path.exists(write_val_images_path):  # if there isn't this directory, make a new one
        os.makedirs(write_val_images_path)
    if not os.listdir(write_val_images_path):  # if the directory is empty, it needs new image data
        CocoExtract().extract_images(read_json_path=write_val_json_path, read_images_path=read_val_images_path,
                                     write_images_path=write_val_images_path, download=True)


# checkpoint and its corresponding url for downloading
# It's from the link https://github.com/open-mmlab/mmdetection/blob/master/docs/zh_cn/model_zoo.md
checkpoint_url = {'faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth':
                      'https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth',
                  'mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth':
                      'https://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_fpn_1x_coco/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth'}


@pytest.fixture(scope='function')
def prep_checkpoint(request):
    """
    Function: download all the checkpoint needed in one time

    """
    checkpoint_file = request.param[1].split('/')[1]  # checkpoint is at this place
    url = checkpoint_url[checkpoint_file]
    path = os.path.join(pytest.CODEB_PATH, 'checkpoints')
    if not os.path.exists(path):
        # make the checkpoints directory which contains all the checkpoints we will download
        os.makedirs(path)
    path = os.path.join(path, checkpoint_file)
    if not os.path.exists(path):
        r = requests.get(url)
        print("Start downloading checkpoint file")
        open(path, 'wb').write(r.content)
        print("Finish downloading checkpoint file")

    return 0
