from argparse import Action
import pytest
from git import Repo
import util

pytest.CODE_PATH = "/opt/mmdeploy"


def pytest_addoption(parser):
    parser.addoption("--mmdet", action="store", default="master", help="mmdet branch option: branch name or tag name")
    parser.addoption("--mmcls", action="store", default="master", help="mmcls branch option: branch name or tag name")


@pytest.fixture(scope="module")
def mmdet(request):
    mmdet_version = request.config.getoption("--mmdet")
    return (util.MMDET_CB, mmdet_version)


@pytest.fixture(scope="module")
def mmcls(request):
    mmcls_version = request.config.getoption("--mmcls")
    return (util.MMCLS_CB, mmcls_version)


def pytest_configure(config):
    if config.getoption("--mmdet"):
        Repo.clone_from(util.MMDET_URL, util.CODEBASE_PATH+util.MMDET_CB, branch=config.getoption("--mmdet"))
    if config.getoption("--mmcls"):
        Repo.clone_from(util.MMCLS_URL, util.CODEBASE_PATH+util.MMCLS_CB, branch=config.getoption("--mmcls"))