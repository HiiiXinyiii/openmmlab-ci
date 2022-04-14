import os
import pytest

# route into the layer of mmpose directory
pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../../"))       # for application
# pytest.CODEB_PATH = os.path.abspath(os.path.join(os.getcwd(), "../../../mmhuman3d"))   # for development
