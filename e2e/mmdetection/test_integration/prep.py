import pytest
import os
from ...preparation.prep import *


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
    extractor = DataExtract()

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