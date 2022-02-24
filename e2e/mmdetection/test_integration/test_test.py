"""
Function: It's designed to test file test.py by calling
"""

import logging
import subprocess
from requests.adapters import HTTPAdapter
from .preparation.prep import *

# config checkpoint mode
temp = [('configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py',
         'checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth',
         '--eval proposal'),
        ('configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py',
         'checkpoints/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth',
         '--eval proposal')]
checkpoint_url = {'faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth':
                      'https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth',
                  'mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth':
                      'https://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_fpn_1x_coco/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth'}
def param_config_checkpoint_mode():  # this is not a case
    def download_checkpoint(checkpoint_file):
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
                r = s.get(url, timeout=(3, 20))
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
            tmp.append(i_path[2])       # keep mode
            res.append(tuple(tmp))
        return res

    # download all checkpoints
    print(f"Start downloading ALL checkpoint files")
    for i_parm in temp:
        checkpoint_file = i_parm[1].split('/')[1]    # checkpoint is at this place
        download_checkpoint(checkpoint_file)
    print(f"Finish downloading ALL checkpoint files")

    return adapt_path(temp)


class TestTest:
    """
    Function: test file test.py by calling

    """

    @pytest.mark.usefixtures('prep')
    @pytest.mark.parametrize('config, checkpoint, mode', param_config_checkpoint_mode())
    def test_test_config_checkpoint(self, config, checkpoint, mode):
        """
        Function: test file test.py with parameters [config and checkpoint]

        :param config:
        :param checkpoint:
        """
        file_path = os.path.join(pytest.CODEB_PATH, 'tools/test.py')
        cmd = "python " + file_path + ' ' + config + ' ' + checkpoint + ' ' + mode  # the cmd to be executed
        res = subprocess.run(cmd.split(' '))
        assert res.returncode == 0, \
            f'Failed to run test.py with parameter [config=={config}, checkpoint=={checkpoint}] set '
        logging.getLogger().info("Finish pytest command: " + cmd)

    # @pytest.mark.parametrize('config, checkpoint, mode', param_config_checkpoint_mode())
    # def test_test_acc(self, config, checkpoint, mode):
    #     """
    #     Function: test the accuracy of the model
    #
    #     :return:
    #     """
    #     file_path = os.path.join(pytest.CODEB_PATH, 'tools/test.py')
    #     cmd = "python " + file_path + ' ' + config + ' ' + checkpoint + ' ' + mode  # the cmd to be executed
    #     result = subprocess.run(cmd.split(' '), capture_output=True)
    #     print('*******************************************************')
    #     print(result.stdout)
    #     print('*******************************************************')
    #     # judge whether it runs successfully
    #     assert result.returncode == 0, \
    #         f'Failed to run test.py with parameter [config=={config}, checkpoint=={checkpoint}] set '
    #
    #     # get the acc information
    #     logging.getLogger().info("Finish pytest command: " + cmd)
