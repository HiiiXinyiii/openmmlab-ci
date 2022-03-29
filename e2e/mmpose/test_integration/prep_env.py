import subprocess
import pytest

cmd_envs_level_0 = ["pip install -i https://pypi.douban.com/simple/ mmcv-full",
                    "pip install -i https://pypi.douban.com/simple/ mmtrack",
                    "pip install -i https://pypi.douban.com/simple/ mmdet"
                    ]


@pytest.mark.parametrize('cmd', cmd_envs_level_0)
@pytest.fixture(scope="function")
def prep_env_for_level_0(cmd):
    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, f'FAILED to prepare env of {cmd}'


cmd_envs_level_2 = ["pip install -i https://pypi.douban.com/simple/ face_recognition",
                    ]


@pytest.fixture(scope="function")
@pytest.mark.parametrize('cmd', cmd_envs_level_2)
def prep_env_for_level_2(cmd):
    res = subprocess.run(cmd.split(' '))
    assert res.returncode == 0, f'FAILED to prepare env of {cmd}'
