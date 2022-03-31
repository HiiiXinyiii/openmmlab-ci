import os
import pytest
import subprocess
import logging
import yaml
from ....utils import utils


def get_command():
    command = [
        # *********************************** 3d_body_mesh_demo.md ***********************************
        # NOT COMPLETE!!!!!!!!
        # # Here, we need to copy the model file "smpl_mean_params.npz" to the path set by config to test
        # "python " + os.path.join(pytest.CODEB_PATH, "demo/mesh_img_demo.py") + " "
        # + os.path.join(pytest.CODEB_PATH, "configs/body/3d_mesh_sview_rgb_img/hmr/mixed/res50_mixed_224x224.py") + " "
        # + str(resources['test_demo']['3d_body_mesh_demo']['checkpoints'][0]['url']) + " "
        # + "--json-file " + os.path.join(pytest.CODEB_PATH, "tests/data/h36m/h36m_coco.json") + " "
        # + "--img-root " + os.path.join(pytest.CODEB_PATH, "tests/data/h36m") + " "
        # + "--out-img-root " + os.path.join(pytest.CODEB_PATH, "vis_results"),
    ]

    return command


@pytest.mark.parametrize('cmd', get_command())
def test_3d_body_mesh_demo(cmd):
    logging.getLogger().info(f"START pytest command: {cmd}")

    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, \
        f'FAILED to run demo with command like {cmd}'

    logging.getLogger().info(f"FINISH pytest command: {cmd}")
