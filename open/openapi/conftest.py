import logging
import pytest
from openapi.client import HttpClient, ApiClient


@pytest.fixture(scope="module")
def hc(request):
    try:
        hc = HttpClient()
        # TODO:
        hc.set_valid_pair("PWZMAl6EmSpb8EyxZ86LmwJ5", "Dy1vMzmVGC13BA7pOBnWX0Nk")
        hc.set_invalid_pair("invalid", "Dy1vMzmVGC13BA7pOBnWX0Nk")
    except Exception as e:
        logging.getLogger().error(str(e))
        pytest.exit("Init http client failed.")

    def fin():
        try:
            pass
        except Exception as e:
            logging.getLogger().info(str(e))

    request.addfinalizer(fin)
    return hc


@pytest.fixture(scope="module")
def ac(request):
    try:
        hc = HttpClient()
        # TODO:
        hc.set_valid_pair("PWZMAl6EmSpb8EyxZ86LmwJ5", "Dy1vMzmVGC13BA7pOBnWX0Nk")
        c = ApiClient()
    except Exception as e:
        logging.getLogger().error(str(e))
        pytest.exit("Init api client failed.")

    def fin():
        try:
            pass
        except Exception as e:
            logging.getLogger().info(str(e))

    request.addfinalizer(fin)
    return c