import os
import pytest
import platform


# the codebase directory
if platform.system().lower() == 'windows':
    pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
elif platform.system().lower() == 'linux':
    pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd()))

pytest.MMDET_PATH = os.getcwd()

# whether to test all configs
pytest.test_all_configs = False          # if it's set to be True, we will pytest all the config files in the codebase
# pytest.test_config_num = 10             # it works when pytest.test_all_configs == True
