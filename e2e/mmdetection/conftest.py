import os
import pytest
import platform
import re

# the codebase directory
if platform.version().lower[platform.version().lower().find('~'):platform.version().lower().find('~')+2] == '18':
    pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../../"))
elif platform.version().lower[platform.version().lower().find('~'):platform.version().lower().find('~')+2] == '16':
    pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd()))

pytest.MMDET_PATH = os.getcwd()

# whether to test all configs
pytest.test_all_configs = False          # if it's set to be True, we will pytest all the config files in the codebase
# pytest.test_config_num = 10             # it works when pytest.test_all_configs == True
