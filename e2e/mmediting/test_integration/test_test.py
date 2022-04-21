import pytest
import os
import sys
import subprocess
import logging

sys.path.append("..")
from utils import utils     # it may show error, but it will work since we have used sys.path.append


def param_cfg_cpt():
    """
    Function: get the param that fits the directory structure

    """

    # (config and checkpoint)
    params = [(os.path.join(pytest.CODEB_PATH, "configs/restorers/basicvsr_plusplus/basicvsr_plusplus_c64n7_8x1_600k_reds4.py"),
               utils.get_cpt(file_path="configs/restorers/basicvsr_plusplus/basicvsr_plusplus_c64n7_8x1_600k_reds4.py",
                             code_path=pytest.CODEB_PATH))
               # (os.path.join(pytest.CODEB_PATH, "configs/restorers/real_basicvsr/realbasicvsr_c64b20_1x30x8_lr5e-5_150k_reds.py"),
               #  utils.get_cpt(file_path="configs/restorers/real_basicvsr/realbasicvsr_c64b20_1x30x8_lr5e-5_150k_reds.py",
               #                code_path=pytest.CODEB_PATH))
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
    Function: Test test.py

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
        cmd = "python" + " " + file_path + ' ' + cmd_param + " " \
              + "--cfg-options data.workers_per_gpu=1 log_config.interval=2 total_iters=1 " \
              + "data.train.dataset.num_input_frames=2 data.val.num_input_frames=2 data.test.num_input_frames=2"

        # execute the command
        logging.getLogger().info("START to pytest command: " + cmd)

        res = subprocess.run(cmd.split())
        assert res.returncode == 0, \
            f'Failed to run test.py with {cmd}'

        logging.getLogger().info("FINISH pytest command: " + cmd)
