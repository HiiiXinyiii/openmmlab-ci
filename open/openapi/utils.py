import logging
import os
import pdb
import time
import json
import random
import string
import hashlib
import traceback
import threading
import logging
import requests
from . import constants


def gen_uniq_str(str_value=None):
    prefix = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    return "test_" + prefix if str_value is None else str_value + "_" + prefix


def gen_invalid_pairs():
    return constants.INVALID_FORMAT_PAIRS


class Auths():
    def __init__(self) -> None:
        pass

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

    def get_token(self, ak=None, sk=None):
        ts = str(int(time.time()))
        nonce = gen_uniq_str()
        access_key = ak if ak is not None else self.valid_pair[0]
        secret_key = sk if sk is not None else self.valid_pair[1]
        concat_string = "uri=%s&ts=%s&nonce=%s&accessKey=%s&secretKey=%s" % (constants.AUTH_URI, ts, nonce, access_key, secret_key)
        sign = hashlib.sha256(concat_string.encode("utf-8")).hexdigest()
        url = constants.OPENAPI_SERVER + constants.USER_SERVICE + constants.AUTH_URI
        headers = {
            "ts": ts,
            "nonce": nonce,
            "sign": sign,
            "accessKey": access_key
        }
        try:
            ret = requests.post(url, headers=headers)
            content = json.loads(ret.content)
            return content["data"]["accessToken"]
        except:
            logging.error(traceback.format_exc())
            raise

    def create_new_pair(self):
        url = constants.OPENAPI_SERVER + constants.USER_SERVICE + constants.AUTH_CREATE_URI
        try:
            ret = requests.post(url)
            logging.info(ret.content)
            content = json.loads(ret.content)
            return (content["data"]["accessKey"], content["data"]["secretKey"])
        except:
            logging.error(traceback.format_exc())
            raise


class TestThread(threading.Thread):
    def __init__(self, target, args=()):
        threading.Thread.__init__(self, target=target, args=args)

    def run(self):
        self.exc = None
        try:
            super(TestThread, self).run()
        except BaseException as e:
            self.exc = e
            logging.error(traceback.format_exc())

    def join(self):
        super(TestThread, self).join()
        if self.exc:
            raise self.exc