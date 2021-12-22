import logging
import pytest
from openapi import constants

from openapi import utils
from openapi.client import ApiClient

logger = logging.getLogger("openapi.apis.upload_test")


class TestUpload:
    """Test cases for uploading in open-apis
    """
    # def __init__(self) -> None:
    #     self.c = ApiClient()

    @pytest.fixture(
        scope="function",
        params=utils.gen_invalid_pairs()
    )
    def get_invalid_pair(self, request):
        yield request.param

    def test_upload_with_invalid_header(self, ac):
        """Checking response if using the invalid header.
        Expected: upload failed, code: 
        """
        headers = {}
        # with pytest.raises(Exception) as e: 
        res = ac.upload_file(headers=headers, codebase=constants.DEFAULT_CODEB, filename=constants.DEFAULT_FILE)
        logging.getLogger().debug(res)
        assert not res["data"]

    def test_upload_with_invalid_token(self, ac):
        """Checking response if using the invalid token.
        Expected: upload failed, code: 
        """
        headers = {"Authorization": "invalid token"}
        with pytest.raises(Exception) as e: 
            res = ac.upload_file(headers=headers, codebase=constants.DEFAULT_CODEB, filename=constants.DEFAULT_FILE)

    def test_upload_with_invalid_codebase(self, ac):
        """Checking response if using the invalid codebase tag.
        Expected: upload failed, code: 
        """
        res = ac.upload_file(codebase="invalid", filename=constants.DEFAULT_FILE)
        logging.getLogger().debug(res)
        assert not res["data"]

    def test_upload_with_invalid_key(self, ac):
        """Checking response if using the invalid key.
        Expected: upload failed, code: 
        """
        # TODO:
        pass            

    def test_upload(self, ac):
        """Checking response if using the valid params.
        Expected: upload success, code: 
        """
        res = ac.upload_file(codebase=constants.DEFAULT_CODEB, filename=constants.DEFAULT_FILE)
        logging.getLogger().info(res)
        assert res["data"]["fileId"]
        assert res["data"]["fileUrl"]

    def test_upload_twice(self, ac):
        """Checking response if using the valid params twice.
        Expected: upload success and get the different result, code: 
        """
        res = ac.upload_file(codebase=constants.DEFAULT_CODEB, filename=constants.DEFAULT_FILE)
        logging.getLogger().info(res)
        res_new= ac.upload_file(codebase=constants.DEFAULT_CODEB, filename=constants.DEFAULT_FILE)
        logging.getLogger().info(res_new)
        assert res["data"] == res_new["data"]

    
class TestAdvanced:
    pass