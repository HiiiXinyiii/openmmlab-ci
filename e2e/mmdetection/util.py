import random
import string


def gen_uniq_str(str_value=None):
    prefix = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    return "test_" + prefix if str_value is None else str_value + "_" + prefix
