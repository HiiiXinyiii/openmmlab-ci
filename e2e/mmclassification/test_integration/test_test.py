import pytest
import os
import sys
import subprocess
import logging
import requests
from multiprocessing import Pool
from requests.adapters import HTTPAdapter

sys.path.append("..")
from utils import utils     # it may show error, but it will work since we have used sys.path.append


@pytest.fixture(scope="session")
def get_dataset():
    def download_image(url, filepath):
        """
        Function:

        :return: No exception: 0;  Exception: exception
        """

        # download the file
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        r = None
        try:
            r = s.get(url=url, timeout=(3, 50))
        except Exception as e:      # except requests.exceptions.RequestException as e:
            logging.getLogger().error(e)
            return e
            # assert False, f'Fail to download the image {i_image["file_name"]} from url \"{i_image["coco_url"]}\"'

        # save the file
        try:
            f = open(filepath, 'wb')
            f.write(r.content)
            f.close()
        except Exception as e:
            logging.getLogger().error(f"Fail to download into {filepath}")
            return e
        return 0

    # tuple(link and directory to save)
    datasets = [("https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz", "data/cifar10")]

    result_download = []

    pool = Pool()
    for i_url, i_path in datasets:
        if not os.path.exists(i_path):
            os.makedirs(i_path)
        file_name = i_url.split('/')[-1]
        filepath = os.path.join(i_path, file_name)
        # download_image(url=i_url, filepath=filepath)
        result_download.append(pool.apply_async(download_image, args=(i_url, filepath,)))
    pool.close()
    pool.join()

    for i_res in result_download:
        tmp = i_res.get()
        if not isinstance(tmp, int) or tmp != 0:
            assert False, f'Fail to download dataset!'

    return True


@pytest.mark.usefixtures("get_dataset")
def param_cfg_cpt():
    """
    Function: get the param that fits the directory structure

    """

    # (config and checkpoint)
    params = [(os.path.join(pytest.CODEB_PATH, "configs/resnet/resnet18_8xb16_cifar10.py"),
               utils.get_cpt(file_path="configs/resnet/resnet18_8xb16_cifar10.py",
                             code_path=pytest.CODEB_PATH)),
              (os.path.join(pytest.CODEB_PATH, "configs/resnet/resnet50_8xb32_in1k.py"),
               utils.get_cpt(file_path="configs/resnet/resnet50_8xb32_in1k.py",
                             code_path=pytest.CODEB_PATH))
              ]

    res = []
    for i_param in params:
        tmp = ""
        for j_part in i_param:
            tmp = tmp + str(j_part) + " "

        res.append(tmp.strip())

    return res


class TestTest:
    """
    Function: Test train.py

    """

    @pytest.mark.parametrize('cmd_param', param_cfg_cpt())
    def test_test_config_checkpoint(self, cmd_param):
        """
        Function: test test.py

        :param cmd_param: the command user use to call test.py
        :return:
        """

        file_path = os.path.join(pytest.CODEB_PATH, 'tools/test.py')
        # the cmd to be executed
        cmd = "python" + " " + file_path + ' ' + cmd_param \
              + " " + "--out result.json" + " " + "--metrics accuracy" + " " \
              + "--cfg-options data.workers_per_gpu=1 data.samples_per_gpu=64"

        # execute the command
        logging.getLogger().info("START to pytest command: " + cmd)

        res = subprocess.run(cmd.split())
        assert res.returncode == 0, \
            f'Failed to run train.py with {cmd}'

        logging.getLogger().info("FINISH pytest command: " + cmd)
