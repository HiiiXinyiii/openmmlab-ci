import os
import pytest
import shutil
from ...preparation.prep import *


@pytest.fixtures(scope="module")
def prepare_data(scr_path="data", des_dir_path=pytest.CODEB_PATH):
    """
    Function: Copy the data to the root directory of mmpose

    """
    # destination file or directory path
    des_dir_path = os.path.join(des_dir_path, scr_path)

    # copy the all files (including the directory and the files in it)
    shutil.copytree(scr_path, des_dir_path)


# prepare the data and save it in the ci remote repo
def _extract_data():
    """
    Function: extract some data including json and images from the all

    :param src_path:
    :param des_path:

    Note: For internal use. Remember to change the filename of the result back to the name you want
    """
    # the extractor
    extractor = DataExtract()
    read_train_json_path = "../data/animalpose/original/annotations/animalpose_train.json"
    write_train_json_path = "../data/animalpose/annotations/animalpose_train.json"
    read_train_images_path = "../data/animalpose/original/images"
    write_train_images_path = "../data/animalpose"

    # extract the json file
    extractor.extract_json(read_json_path=read_train_json_path, write_json_path=write_train_json_path, size=120)

    # extract the image
    extractor.extract_images(read_json_path=write_train_json_path,
                             read_images_path=read_train_images_path, write_images_path=write_train_images_path,
                             download=False)


if __name__ == '__main__':
    _extract_data()

