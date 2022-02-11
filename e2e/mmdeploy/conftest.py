from argparse import Action
import pytest

pytest.CODE_PATH = "/opt/mmdeploy"


def pytest_addoption(parser):
    parser.addoption("--mmdet", action="store", default="master", help="mmdet branch option: branch name or tag name")
    parser.addoption("--mmcls", action="store", default="master", help="mmcls branch option: branch name or tag name")


@pytest.fixture(scope="module")
def mmdet(request):
    mmdet_version = request.config.getoption("--mmdet")
    return ("mmdetection", mmdet_version)


@pytest.fixture(scope="module")
def mmcls(request):
    mmcls_version = request.config.getoption("--mmcls")
    return ("mmclassification", mmcls_version)