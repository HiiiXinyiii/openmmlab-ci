"""
Function: It's designed to test file test.py by calling
"""

import logging
import subprocess
from .preparation.prep import *


# config checkpoint mode
temp = [('configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py', 'checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth', '--format-only'),
        ('configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py', 'checkpoints/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth', '--format-only')]
@pytest.mark.parametrize('prep_checkpoint', temp, indirect=True)
def param_config_checkpoint():          # this is not a case
    return temp


class TestTest:
    """
    Function: test file test.py by calling

    """

    @pytest.mark.parametrize('config, checkpoint, mode', param_config_checkpoint())
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
