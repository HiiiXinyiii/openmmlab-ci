import pytest
import os
import subprocess
import logging


def param_config():
    """
    Function: get the param that fits the directory structure

    """

    # to make it fit the server directory
    def adapt_path(path):
        """
        Function: to make it fit the server directory

        :param path: the the config file path from the root
        """
        res = []
        for i_path in path:
            res.append(os.path.join(pytest.CODEB_PATH, i_path))
        return res

    params = ["configs/restorers/basicvsr_plusplus/basicvsr_plusplus_c64n7_8x1_600k_reds4.py",
              "configs/restorers/real_basicvsr/realbasicvsr_c64b20_1x30x8_lr5e-5_150k_reds.py"]

    return adapt_path(params)


class TestTrain:
    """
    Function: Test train.py

    """

    @pytest.mark.parametrize('cmd_param', param_config())
    def test_train_config(self, cmd_param):
        """
        Function: test train.py

        :param cmd_param: the command user use to call train.py
        :return:
        """

        file_path = os.path.join(pytest.CODEB_PATH, 'tools/train.py')
        # the cmd to be executed
        cmd = "python" + " " + file_path + " " + cmd_param + " " \
              + "--cfg-options data.workers_per_gpu=1 log_config.interval=2 total_iters=1" + " " \
              + "data.train.dataset.num_input_frames=2 data.val.num_input_frames=2 data.num_input_frames=2"

        # execute the command
        logging.getLogger().info("START to pytest command: " + cmd)

        res = subprocess.run(cmd.split())
        assert res.returncode == 0, \
            f'Failed to run train.py with cmd as {cmd}'

        logging.getLogger().info("FINISH pytest command: " + cmd)
