from argparse import Action
import pytest

pytest.CODE_PATH = "/opt/mmdeploy"


def pytest_addoption(parser):
    parser.addoption("--mmdet", action="store", default="master", help="mmdet branch option: branch name or tag name")
    parser.addoption("--mmcls", action="store", default="master", help="mmcls branch option: branch name or tag name")


@pytest.fixture
def mmdet(request):
    return ("mmdetection", request.config.getoption("--mmdet"))


@pytest.fixture
def mmcls(request):
    return ("mmclassification", request.config.getoption("--mmcls"))