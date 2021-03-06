import os
import requests
from requests.adapters import HTTPAdapter
import pytest
import logging
import subprocess


checkpoint_url = {"res50_animalpose_256x256-e1f30bff_20210426.pth":
                      "https://download.openmmlab.com/mmpose/animal/resnet/res50_animalpose_256x256-e1f30bff_20210426.pth"}

params = [('configs/animal/2d_kpt_sview_rgb_img/topdown_heatmap/animalpose/res101_animalpose_256x256.py',
           'checkpoints/res50_animalpose_256x256-e1f30bff_20210426.pth')
          ]


def param_config_checkpoint():
    def download_checkpoint(checkpoint_file):
        """

        Note: Download path = os.path.join(pytest.CODEB_PATH, 'checkpoints')
        """
        url = checkpoint_url[checkpoint_file]
        path = os.path.join(pytest.CODEB_PATH, 'checkpoints')
        if not os.path.exists(path):
            # make the checkpoints directory which contains all the checkpoints we will download
            os.makedirs(path)
        path = os.path.join(path, checkpoint_file)
        if not os.path.exists(path):
            # Download the file
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            r = None        # save the content of the checkpoint
            try:
                r = s.get(url, timeout=(10, 20))
            except requests.exceptions.RequestException as e:
                logging.getLogger().error(f'Fail to download checkpoint file [{checkpoint_file}]')
                assert False, f'Fail to download checkpoint file [{checkpoint_file}]'
            # write content
            try:
                with open(path, 'wb')as f:
                    f.write(r.content)
            except FileNotFoundError:
                logging.getLogger().error(f'Fail to save checkpoint file [{checkpoint_file}]')
                assert False, f'Fail to save checkpoint file [{checkpoint_file}]'
            print(f"Finish downloading and saving checkpoint file [{checkpoint_file}]")
        return 0

    # to make it fit the server directory
    def adapt_path(path):
        res = []
        for i_path in path:
            tmp = list(os.path.join(pytest.CODEB_PATH, i) for i in i_path[0:2])    # modify config and checkpoint
            res.append(tuple(tmp))
        return res

    # download all checkpoints
    print(f"Start downloading ALL checkpoint files")
    logging.getLogger().info(f"START downloading ALL checkpoint files")
    for i_parm in params:
        checkpoint_file = i_parm[1].split('/')[1]    # checkpoint is at this place
        download_checkpoint(checkpoint_file)
    print(f"Finish downloading ALL checkpoint files")
    logging.getLogger().info(f"FINISH downloading ALL checkpoint files")

    return adapt_path(params)


class TestTest:
    @pytest.mark.parametrize('config, checkpoint', param_config_checkpoint())
    def test_test_config_checkpoint(self, config, checkpoint):
        """
        Function: test file test.py with parameters [config and checkpoint]

        :param config:
        :param checkpoint:

        """
        file_path = os.path.join(pytest.CODEB_PATH, 'tools/test.py')
        # the cmd to be executed
        cmd = "python " + file_path + ' ' + config + ' ' + checkpoint
        # execute the command
        logging.getLogger().info("START pytest command: " + cmd)
        res = subprocess.run(cmd.split(' '))
        assert res.returncode == 0, \
            f'Failed to run test.py with parameter [config=={config}, checkpoint=={checkpoint}] set '
        logging.getLogger().info("Finish pytest command: " + cmd)


