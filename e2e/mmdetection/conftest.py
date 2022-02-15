import os
import pytest
import platform

# the codebase directory (decide it by system version, server=18.04[4.15.0-143-generic], local=16.04)
if platform.version().lower()[platform.version().lower().find('~')+1:platform.version().lower().find('~')+3] == '16':
    pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd()))
else:
    pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../../"))

# the mmdetection directory path for us to find data directory
pytest.MMDET_PATH = os.getcwd()

# whether to test all configs
pytest.test_all_configs = False          # if it's set to be True, we will pytest all the config files in the codebase
# pytest.test_config_num = 10             # it works when pytest.test_all_configs == True
