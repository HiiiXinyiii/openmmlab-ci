import subprocess
import pytest
import logging
import shutil
import os


@pytest.fixture(scope="session")
def prep_others():
    # for 3d_body_mesh_demo.md
    shutil.copy2(os.path.join(pytest.CODEB_PATH, "tests/data/smpl/smpl_mean_params.npz"),
                 "models/smpl/smpl_mean_params.npz")


@pytest.fixture(scope="session")
def prep_env_for_level_0():
    cmd_envs_level_0 = ["pip install -i https://pypi.douban.com/simple/ mmcv-full",
                        "pip install -i https://pypi.douban.com/simple/ mmtrack",
                        "pip install -i https://pypi.douban.com/simple/ mmdet"
                        ]
    for cmd in cmd_envs_level_0:
        logging.getLogger().info("START Install the Environment: " + cmd)
        res = subprocess.run(cmd.split(' '))
        assert res.returncode == 0, f'FAILED to prepare env of {cmd}'
        logging.getLogger().info("FINISH Install the Environment: " + cmd)


@pytest.fixture(scope="session")
def prep_env_for_level_2():
    cmd_envs_level_2 = ["pip install -i https://pypi.douban.com/simple/ face_recognition",
                        ]

    for cmd in cmd_envs_level_2:
        logging.getLogger().info("START Install the Environment: " + cmd)
        res = subprocess.run(cmd.split(' '))
        assert res.returncode == 0, f'FAILED to prepare env of {cmd}'
        logging.getLogger().info("Finish Install the Environment: " + cmd)
