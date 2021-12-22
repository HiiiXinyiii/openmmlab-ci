import logging
import random
import string
import traceback
import threading
import logging
from requests import get, put, delete, post

from openapi import constants

logger = logging.getLogger("openapi.utils")


def gen_uniq_str(str_value=None):
    prefix = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    return "test_" + prefix if str_value is None else str_value + "_" + prefix


def gen_invalid_pairs():
    return constants.INVALID_FORMAT_PAIRS


def gen_invalid_urls():
    return [
        # 404
        constants.DEFAULT_FILE_URL+"aa",
        " ",
        "",
        [constants.DEFAULT_FILE_URL, constants.DEFAULT_FILE_URL]
    ]


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