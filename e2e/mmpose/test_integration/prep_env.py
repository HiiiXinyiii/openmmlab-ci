import subprocess
import pytest
import logging


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
