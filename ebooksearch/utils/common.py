# encoding: utf-8
__author__ = '得一'

import hashlib
import re


def get_md5(url) :
    # md5 加密
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5(url)
    return m.hexdigest()