import os
import sys
import time
import logging
import copy
import json
import hashlib
import traceback

from requests import get, put, delete, post
from requests.exceptions import HTTPError
from openapi import constants
from openapi import utils

logger = logging.getLogger("openapi.client")


class HttpClient(object):
    """
    Base http-client class for requests
    """
    def __init__(self, host=None, verify_ssl=None):
        self.host = host if host else constants.OPENAPI_SERVER

        self.method_kwargs = {}
        if verify_ssl is not None:
            self.method_kwargs['verify'] = verify_ssl

    @property
    def valid_pair(self):
        return (os.environ.get("V_AK"), os.environ.get("V_SK"))

    @property
    def invalid_pair():
        return (os.environ.get("IV_AK"), os.environ.get("IV_SK"))

    def set_valid_pair(self, ak, sk):
        os.environ["V_AK"] = ak
        os.environ["V_SK"] = sk
    
    def set_invalid_pair(self, ak, sk):
        os.environ["IV_AK"] = ak
        os.environ["IV_SK"] = sk 

    def _get_token(self, ak=None, sk=None):
        ts = str(int(time.time()))
        nonce = utils.gen_uniq_str()
        access_key = ak if ak is not None else self.valid_pair[0]
        secret_key = sk if sk is not None else self.valid_pair[1]
        concat_string = "uri=%s&ts=%s&nonce=%s&accessKey=%s&secretKey=%s" % (constants.AUTH_URI, ts, nonce, access_key, secret_key)
        sign = hashlib.sha256(concat_string.encode("utf-8")).hexdigest()
        url = constants.USER_SERVICE+constants.AUTH_URI
        headers = {
            "ts": ts,
            "nonce": nonce,
            "sign": sign,
            "accessKey": access_key
        }
        try:
            content = self._http_call(url, post, headers=headers)
            return content["data"]["accessToken"]
        except:
            logger.error(traceback.format_exc())
            raise

    def _create_new_pair(self):
        url = constants.USER_SERVICE+constants.AUTH_CREATE_URI
        try:
            content = self._http_call(url, post)
            return (content["data"]["accessKey"], content["data"]["secretKey"])
        except:
            logger.error(traceback.format_exc())
            raise

    def _http_response(self, url, method, headers=None, data=None, files=None, **kwargs):
        """
        @pramas: url, full target url
               : method, method from requests
               : data, request body
               : kwargs, url formatting args
        """
        if not files and data:
            data = json.dumps(data)
        path = url.format(**kwargs)
        logger.debug("%s %s", method.__name__.upper(), path)
        response = method(self.host+path,
                        data=data, files=files, headers=headers, **self.method_kwargs)
        logger.debug("<status code: %s> %s", response.status_code, response.reason)
        response.raise_for_status()
        return response

    def _http_call(self, url, method, headers=None, data=None, files=None, **kwargs):
        response = self._http_response(url, method, headers=headers, data=data, files=files, **kwargs)
        if not response.content:
            return {}
        logger.error(response.headers)
        logger.error(response.content)
        return response.json()


class ApiClient(HttpClient):
    def __init__(self, *args, **kwargs):
        super(ApiClient, self).__init__(*args, **kwargs)

    def request(self, codeb, headers=None, body=None, filetype=constants.FILE_TYPE.ID):
        token = self._get_token()
        headers = headers if headers is not None else {
            "Authorization": token,
            'Content-type': "application/json"
        }
        url = constants.INF_SERVICE+constants.API_URI+codeb.value
        # generate the request body for resourceType `ID`
        if body is None:
            cdata = self.upload_file(codebase=codeb, filename=constants.DEFAULT_FILE_ID)["data"]
            if filetype == constants.FILE_TYPE.ID:
                resource = cdata["fileId"]
            elif filetype == constants.FILE_TYPE.URL:
                resource = cdata["fileUrl"]
            body = self.set_body(codeb, {
                "resourceType": filetype.value,
                "resource": resource
            })
            logger.error(body)
        logger.error(headers)
        content = self._http_call(url, post, headers=headers, data=body)
        # content = requests.post(constants.OPENAPI_SERVER+url, headers=headers, json=body)
        return content

    def set_body(self, codeb, kv=None):
        tmp = None
        if codeb == constants.CODEB.CLS:
            tmp = copy.deepcopy(constants.DEFAULT_CLS_BODY)
        elif codeb == constants.CODEB.DET:
            tmp = copy.deepcopy(constants.DEFAULT_DET_BODY)
        elif codeb == constants.CODEB.SEG:
            tmp = copy.deepcopy(constants.DEFAULT_SEG_BODY)
        elif codeb == constants.CODEB.SUP:
            tmp = copy.deepcopy(constants.DEFAULT_SUP_BODY)
        elif codeb == constants.CODEB.POSE:
            tmp = copy.deepcopy(constants.DEFAULT_POSE_BODY)
        elif codeb == constants.CODEB.ACTION:
            tmp = copy.deepcopy(constants.DEFAULT_ACTION_BODY)
        if tmp is None:
            raise Exception("Not supported codeb % " % codeb.value)
        if kv is not None:
            tmp.update(kv)
        return tmp

    def upload_file(self, headers=None, codebase=None, filename=None, new_token=True):
        url = constants.UPLOAD_SERVICE+constants.UPLOAD_URI+"?key=inference&tag=%s" % codebase.value
        token = self._get_token() if new_token is True else constants.DEFAULT_TOKEN
        headers = headers if headers is not None else {
            "Authorization": token
        }
        
        try:
            filepath = os.path.join(os.getcwd(), "assets", filename)
            # import pdb; pdb.set_trace()
            files = [
                ("file", (filename, open(filepath, "rb"), "image/jpeg"))
            ]
            content = self._http_call(url, post, headers=headers, files=files)
            # url = constants.OPENAPI_SERVER+url
            # import requests
            # response = requests.post(url, headers=headers, files=data)
            # print(response.headers)
            # content = response.json()
            return content
        except:
            logger.error(traceback.format_exc())
            raise

    def upload_files(self, codebase=None, file_cnt=2):
        l = []
        for i in range(file_cnt):
            l.append(self.upload_file(codebase=codebase))
        return l

    def get_async_result(self, headers=None, task_id=None):
        url =  constants.INF_SERVICE+constants.ASYNC_RESULT
        token = self._get_token()
        headers = headers if headers is not None else {
            "Authorization": token
        }
        try:
            content = self._http_call(url, post, headers=headers)
            return content
        except:
            logging.error(traceback.format_exc())
            raise