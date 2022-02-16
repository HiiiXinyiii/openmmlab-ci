"""
File description:
It's designed to test train.py from the codebase
"""

import logging
import subprocess
import pytest
from .preparation.prep import *


def param_config():
    """
    Function: the param that train.py needs
    """
    if pytest.test_all_configs:
        return get_all_config_path()
    else:
        def adapt_path(path):
            for i_path in path:
                i_path = os.path.join(pytest.CODEB_PATH, i_path)
            return path

        # we think the work directory is 'mmdetection' in default. We will use the path after modification
        return adapt_path([
            'configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py',
            'configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py',
            'configs/resnest/faster_rcnn_s50_fpn_syncbn-backbone+head_mstrain-range_1x_coco.py'
        ])


class TestTrain:
    @pytest.mark.usefixtures('prep')
    @pytest.mark.parametrize('cmd_param', param_config())
    def test_train_config(self, cmd_param):
        """
        Function: test train.py

        :param cmd_param: the command user use to call train.py
        :return:
        """
        file_path = os.path.join(pytest.CODEB_PATH, 'tools/train.py')
        cmd = "python " + file_path + ' ' + cmd_param  # the cmd to be executed
        assert subprocess.run(cmd.split(' ')).returncode == 0, \
            'Failed to run train.py with parameter [config] set'
        logging.getLogger().info("Finish pytest command: ", cmd)


if __name__ == '__main__':
    print(get_all_config_path())
