"""
Function: It's designed to test file test.py by calling
"""

import logging
import subprocess
from .preparation.prep import *

# config checkpoint mode
temp = [('configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py',
         'checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth', '--eval proposal'),
        (
        'configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py', 'checkpoints/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth',
        '--eval proposal')]
@pytest.mark.parametrize('prep_checkpoint', temp, indirect=True)
def param_config_checkpoint_mode():  # this is not a case
    def adapt_path(path):
        res = []
        for i_path in path:
            tmp = list(os.path.join(pytest.CODEB_PATH, i) for i in i_path[0:2])    # modify config and checkpoint
            tmp.append(i_path[2])       # keep mode
            res.append(tuple(tmp))
        return res
    return adapt_path(temp)


class TestTest:
    """
    Function: test file test.py by calling

    """

    @pytest.mark.parametrize('config, checkpoint, mode', param_config_checkpoint_mode())
    def test_test_config_checkpoint(self, config, checkpoint, mode):
        """
        Function: test file test.py with parameters [config and checkpoint]

        :param config:
        :param checkpoint:
        """
        file_path = os.path.join(pytest.CODEB_PATH, 'tools/test.py')
        cmd = "python " + file_path + ' ' + config + ' ' + checkpoint + ' ' + mode  # the cmd to be executed
        assert subprocess.run(cmd.split(' ')).returncode == 0, \
            f'Failed to run test.py with parameter [config=={config}, checkpoint=={checkpoint}] set '
        logging.getLogger().info("Finish pytest command: ", cmd)

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
    #     logging.getLogger().info("Finish pytest command: ", cmd)
