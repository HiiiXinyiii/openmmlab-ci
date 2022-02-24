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
class CocoExtract:

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
        r = requests.get(i_image['coco_url'])
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

        Note: parameter 'chosen' seems not to work
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


@pytest.fixture(scope='module')
def prep():
    """
    Function: prepare before

    :return:
    """
    # On server we think the root path is '/opt/mmdetection/openmmlab-ci/e2e/mmdetection/'
    # In this way, we don't have to modify the original config file
    # Because in config, they use 'data/coco/annotations/instances_val2017_full.json' in default
    # But actually this download path is not what the author wants the users to use
    read_train_json_path = os.path.join(os.getcwd(), "data/coco_annotations/instances_train2017.json")
    write_train_json_path = os.path.join(os.getcwd(), "data/coco/annotations/instances_train2017.json")
    read_val_json_path = os.path.join(os.getcwd(), "data/coco_annotations/instances_val2017.json")
    write_val_json_path = os.path.join(os.getcwd(), "data/coco/annotations/instances_val2017.json")
    read_train_images_path = os.path.join(os.getcwd(), "data/coco/train2017")    # use when not download
    write_train_images_path = os.path.join(os.getcwd(), "data/coco/train2017")
    read_val_images_path = os.path.join(os.getcwd(), "data/coco/val2017")        # use when not download
    write_val_images_path = os.path.join(os.getcwd(), "data/coco/val2017")

    # extractor
    extractor = CocoExtract()

    # extract part of train json
    if not os.path.exists(write_train_json_path):
        # delete the existing images which are extracted before
        if os.path.exists(write_train_images_path):
            shutil.rmtree(write_train_images_path)
        extractor.extract_json(read_json_path=read_train_json_path, write_json_path=write_train_json_path,
                                   size=extractor.train_size,
                                   chosen=[i for i in range(extractor.train_size)]
                                   # chosen=[39411, 10701, 66707, 15063, 14117, 53179, 114068, 69805, 42114, 86833, 18851, 82074, 18225, 47125, 70894, 71836, 37976, 71969, 117910, 114090, 44317, 107307, 79391, 8321, 43548, 104204, 5600, 67872, 66374, 47095, 12021, 92035, 11907, 5970, 7176, 33208, 64018, 11168, 74187, 45999, 100313, 29162, 223, 15571, 110726, 44728, 81787, 112076, 16261, 49089, 32430, 79600, 7220, 18301, 27786, 49930, 86005, 51144, 50825, 32567, 21329, 25763, 80461, 99241, 38833, 34788, 1556, 1862, 61109, 94109, 95886, 44739, 59764, 87232, 104637, 118196, 15301, 3662, 25446, 48663, 112596, 10347, 70617, 56502, 34419, 66569, 54094, 4029, 110720, 38413, 9756, 32424, 100485, 96822, 71260, 8636, 82881, 796, 52184, 80280, 92227, 27837, 74839, 66750, 88572, 83542, 19047, 109659, 99647, 95799, 76980, 36298, 61946, 95641, 100905, 108854, 96951, 16303, 36805, 36032]
                                   )
    if not os.path.exists(write_train_images_path):
        os.makedirs(write_train_images_path)
    # if the directory is empty, it needs new image data or the images are not complete
    if not os.listdir(write_train_images_path) \
            or sum(os.path.isfile(i) for i in os.listdir(write_train_images_path)) < extractor.train_size:
        extractor.extract_images(read_json_path=write_train_json_path, read_images_path=read_train_images_path,
                                     write_images_path=write_train_images_path, download=True)

    # extract part of val json
    if not os.path.exists(write_val_json_path):
        # delete the existing images which are extracted before
        if os.path.exists(write_val_images_path):
            shutil.rmtree(write_val_images_path)
        extractor.extract_json(read_json_path=read_val_json_path, write_json_path=write_val_json_path,
                                   size=extractor.val_size,
                                   chosen=[i for i in range(extractor.val_size)]
                                   # chosen=[4764, 820, 4327, 4531, 3952, 3460, 1373, 1513, 2393, 4256, 3773, 455, 2473, 2493, 2781, 1475, 4464, 1631, 2912, 4781, 4896, 4438, 568, 918, 1177, 2109, 2200, 1939, 3545, 3629, 2968, 3641, 4298, 2006, 4520, 4439, 4825, 1842, 4121, 3032, 2203, 3557, 3513, 3925, 3849, 1139, 3530, 3798, 780, 2242, 3120, 1323, 2880, 4433, 2199, 4377, 3097, 891, 1237, 1172, 3066, 23, 3047, 3917, 200, 109, 4315, 2398, 4562, 3456, 4637, 3374, 999, 3140, 4112, 2732, 3172, 4159, 591, 2861, 1970, 2132, 2282, 3793, 1807, 2687, 63, 45, 308, 3938, 605, 4078, 1578, 2733, 2217, 157, 2535, 3163, 4523, 2641, 505, 3563, 2668, 1374, 877, 1660, 920, 2969, 1700, 2310, 1683, 3007, 880, 55, 3258, 4214, 1856, 1414, 1915, 4383]
                                   )
    # extract part of val images
    if not os.path.exists(write_val_images_path):  # if there isn't this directory, make a new one
        os.makedirs(write_val_images_path)
    # if the directory is empty, it needs new image data or the images are not complete
    if not os.listdir(write_val_images_path) \
            or sum(os.path.isfile(i) for i in os.listdir(write_val_images_path)) < extractor.val_size:
        extractor.extract_images(read_json_path=write_val_json_path, read_images_path=read_val_images_path,
                                     write_images_path=write_val_images_path, download=True)


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
    CocoExtract().extract_json(read_json_path='../../data/coco_annotations/instances_train2017_full.json', write_json_path='./aaa.json',
                               size=120, chosen=[i for i in range(100, 300)])
