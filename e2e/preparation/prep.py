import requests
import json
import shutil
import random
import time
import re
import pytest
import os
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
import logging


# extract part of coco dataset
class DataExtract:

    def __init__(self, train_size=120, val_size=120):
        self.train_size = train_size
        self.val_size = val_size

    def download_image(self, i_image, dir):
        """
        Function:

        :return: No exception: 0;  Exception: exception
        """
        new_filepath = os.path.join(dir, i_image['file_name'])
        # if this image has been downloaded before then quit
        if os.path.exists(new_filepath):
            return 0

        # download the file
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        r = None
        try:
            r = s.get(url=i_image['coco_url'], timeout=(3, 10))
        except Exception as e:      # except requests.exceptions.RequestException as e:
            logging.getLogger().error(e)
            return e
            # assert False, f'Fail to download the image {i_image["file_name"]} from url \"{i_image["coco_url"]}\"'

        # save the file
        try:
            f = open(new_filepath, 'wb')
            f.write(r.content)
            f.close()
        except Exception as e:
            logging.getLogger().error(f"Fail to save the image {new_filepath}")
            # assert False, f'Fail to save image {new_filepath}'
            return e
        return 0

    def extract_json(self, read_json_path, write_json_path, size, chosen=None):
        """
        Function: extract a subset of the coco dataset

        :param chosen:
        :param size:
        :return:

        Note: You may need to modify the fielf of the result.
        """
        try:
            with open(read_json_path, 'r', encoding='utf-8') as fin:
                data_in = json.load(fin)
        except FileNotFoundError:
            assert False, f'Fail to open file {read_json_path} when extracting json from coco dataset'

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
                assert False, 'Type Error! The chosen images should be listed in List'
            for i_image in chosen:
                data_out['images'].append(data_in['images'][i_image])
                images_id_picked.append(data_in['images'][i_image]['id'])

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
            assert False, f'Fail to open file {write_json_path}'

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
            assert False, f'Fail to open file {read_json_path}'

        # if the write_images_path doesn't exist, then create one
        if not os.path.exists(write_images_path):
            os.makedirs(write_images_path)

        # download the images
        if download:
            result = []
            pool = Pool()
            for i_image in data_in['images']:
                result.append(pool.apply_async(self.download_image, args=(i_image, write_images_path, )))
            pool.close()
            pool.join()
            for i_res in result:
                tmp = i_res.get()
                if not isinstance(tmp, int) or tmp != 0:
                    assert False, f'Fail to download images!'

        # if not download, we copy the corresponding images from local directory
        else:
            for i_image in data_in['images']:
                filepath = os.path.join(read_images_path, i_image['file_name'])
                new_filepath = os.path.join(write_images_path, i_image['file_name'])
                shutil.copy2(filepath, new_filepath)


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


# # checkpoint and its corresponding url for downloading
# # It's from the link https://github.com/open-mmlab/mmdetection/blob/master/docs/zh_cn/model_zoo.md
# checkpoint_url = {'faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth':
#                       'https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth',
#                   'mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth':
#                       'https://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_fpn_1x_coco/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth'}
#
#
# @pytest.fixture(scope='function')
# def prep_checkpoint(request):
#     """
#     Function: download all the checkpoint needed in one time
#
#     """
#
#     checkpoint_file = request.param[1].split('/')[1]  # checkpoint is at this place
#     url = checkpoint_url[checkpoint_file]
#     path = os.path.join(pytest.CODEB_PATH, 'checkpoints')
#     if not os.path.exists(path):
#         # make the checkpoints directory which contains all the checkpoints we will download
#         os.makedirs(path)
#     path = os.path.join(path, checkpoint_file)
#     if not os.path.exists(path):
#         r = requests.get(url)
#         print("Start downloading checkpoint file")
#         open(path, 'wb').write(r.content)
#         print("Finish downloading checkpoint file")
#
#     return 0


if __name__ == "__main__":
    DataExtract().extract_json(read_json_path='../../data/coco_annotations/instances_train2017_full.json', write_json_path='./aaa.json',
                               size=120, chosen=[i for i in range(100, 300)])
