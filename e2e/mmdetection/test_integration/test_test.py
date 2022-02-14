"""
Function: It's designed to test file test.py by calling
"""

import logging
import pytest
import subprocess
from prep import *


# config checkpoint
test_param_config_checkpoint = [('configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py', 'faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth')
              ]


class Test_test():
    """
    Function: test file test.py by calling

    """

    @pytest.mark.usefixtures('prep_checkpoint')
    @pytest.mark.parametrize('config, checkpoint', test_param_config_checkpoint)
    def test_test_config_checkpoint(self, config, checkpoint):
        """
        Function: test file test.py with parameters [config and checkpoint]

        :param config:
        :param checkpoint:
        """
        file_path = os.path.join(pytest.CODEB_PATH, 'tools/test.py')
        cmd = "python " + file_path + ' ' + config + ' ' + checkpoint     # the cmd to be executed
        assert subprocess.run(cmd.split(' ')).returncode == 0, \
            'Failed to run test.py with parameter [config, checkpoint] set'
        logging.getLogger().info("Finish pytest command: ", cmd)
