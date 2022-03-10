import os
from pprint import pformat
import pytest
import util
from ...preparation.prep import *


def param_config():
    """
    Function: the param that train.py needs
    """
    # if pytest.test_all_configs:
    #     return get_all_config_path()
    # else:
    # to make it fit the server directory
    def adapt_path(path):
        res = []
        for i_path in path:
            res.append(os.path.join(pytest.CODEB_PATH, i_path))
        return res

    # we think the work directory is 'mmdetection' in default. We will use the path after modification
    return adapt_path([
        'configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'
        # 'configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py',
        # 'configs/resnest/faster_rcnn_s50_fpn_syncbn-backbone+head_mstrain-range_1x_coco.py'
    ])


class TestBenchTrain:
    @pytest.mark.timeout(1000)
    @pytest.mark.usefixtures('prep')
    @pytest.mark.parametrize('cmd_param', param_config())
    def test_benchmark_train(self, cmd_param):
        file_path = os.path.join(pytest.CODEB_PATH, 'tools/train.py')
        cmd = 'python ' + file_path + ' ' + cmd_param \
              + ' --seed=1 --deterministic --cfg-options optimizer.lr=0.002 data.workers_per_gpu=0 data.samples_per_gpu=1 runner.max_epochs=5' # the cmd to be executed
        # execute cmd
        ret_code, ret_msg = util.python_exec(cmd)
        assert ret_code
        logging.getLogger().info(pformat(ret_msg))
        # parse the msg into benchmark metrics
        # TODO