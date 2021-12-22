import logging
import pytest
from openapi import constants
from openapi import utils

logger = logging.getLogger("openapi.apis.cls_test")


class TestCls:
    def setup(self):
        self.codeb = constants.CODEB.CLS

    """Test cases for cls.
    """
    @pytest.fixture(
        scope="function",
        params=utils.gen_invalid_urls()
    )
    def get_invalid_url(self, request):
        yield request.param

    """
        The following cases test the `resource` in body param.
    """
    def test_cls_resource_url(self, ac):
        """Checking response using demo.
        Expected: infer success, code: 
        """
        res = ac.request(self.codeb, filetype=constants.FILE_TYPE.URL)
        assert res["data"]["result"]

    def test_cls_resource_file_id(self):
        """Checking response using demo.
        Expected: infer success, code: 
        """
        res = self.c.request(self.codeb)
        assert res["data"]["result"]

    def test_cls_resource_invalid_url(self, ac, get_invalid_url):
        """Checking response using demo.
        Expected: upload failed, code: 
        """
        body = ac.set_body(self.codeb, {
            "resource": get_invalid_url,
            "resourceType": constants.FILE_TYPE.URL.value,
        })
        # TODO:
        with pytest.raises(Exception) as e: 
            ac.request(self.codeb, body=body)

    def test_cls_resource_invalid_file_id(self, ac, get_invalid_id):
        """Checking response using demo.
        Expected: upload failed, code: 
        """
        body = ac.set_body(self.codeb, {
            "resource": get_invalid_id,
            "resourceType": "ID",
        })
        with pytest.raises(Exception) as e: 
            ac.request(self.codeb, body=body)

    """
        The following cases test the `requestType` in body param.
    """
    def test_cls_request_type_ASYNC(self, ac):
        body = ac.set_body(self.codeb, {
            "requestType": "ASYNC"
        })
        logger.error(body)
        logger.error(ac.request(self.codeb, body=body))
    
    def test_cls_request_type_not_supported(self, ac):
        body = ac.set_body(self.codeb, {
            "requestType": "invalid"
        })
        logger.error(ac.request(self.codeb, body=body))
    
    """
        The following cases test the algorithm_dataset_pair in body param.
    """
    def test_cls_algorithm_dataset(self, get_algorithm_dataset_pairs):
        pass

    def test_cls_algorithm_dataset_not_supported(self, get_invalid_algorithm_dataset):
        pass


class TestAsyncCls():
    def setup(self):
        self.codeb = constants.CODEB.CLS

    def test_cls_aysnc_invalid_task_id(self, ac, get_invalid_task_id):
        """Checking response using demo.
        Expected: infer failed, code: 
        """
        body = ac.set_body(self.codeb, {
            "requestType": "ASYNC",
        })
        task_id = ac.request(self.codeb, body=body)
        ac.get_async_result(task_id)

    def test_cls_aysnc_task_id(self, ac):
        """Checking response using demo.
        Expected: infer success, code: 
        """
        body = ac.set_body(self.codeb, {
            "requestType": "ASYNC",
        })
        task_id = ac.request(self.codeb, body=body)
        ac.get_async_result(task_id)