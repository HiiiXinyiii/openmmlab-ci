import os
import pytest

pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../../"))         # for application
# pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../../mmdetection/"))       # for development

# whether to test all configs
pytest.test_all_configs = False          # if it's set to be True, we will pytest all the config files in the codebase
# pytest.test_config_num = 10             # it works when pytest.test_all_configs == True [not realized]
