# author: Kaan Eraslan
# license: see, LICENSE
# purpose: validate asset documents

import os
import json
import glob
import sys


def read_json(jsonpath: str) -> dict:
    "read json object from given path"
    assert os.path.isfile(jsonpath)
    with open(jsonpath, "r", encoding="utf-8") as fd:
        myfile = json.load(fd)
    return myfile


def validate_simple_authority(author_file: dict) -> bool:
    "given a simple authority file output whether it is valid or not"
    keys = set()
    for author_key, author_value in author_file.items():
        key_type_check = isinstance(author_key, str)
        value_type_check = isinstance(author_value, dict)
        value_length = len(author_value)
        for value_key, value_def in author_value.items():
            vkey_type_check = isinstance(value_key, str)
            vval_type_check = isinstance(value_def, str)
            if (not isinstance(vkey_type_check, str) or
                    not isinstance(vval_type_check, str)):
                return False, author_key, author_value
        if key_type_check is False:
            return False, author_key, author_value
        if value_type_check is False:
            return False, author_key, author_value
        if value_length > 1:
            return False, author_key, author_value
        if author_key not in keys:
            keys.add(author_key)
        else:
            return False, author_key, author_value

def check_simple_authority(author_file: dict):
    "check simple authority file"
    check = validate_simple_authority(author_file)
    if check[0] is False:
        mess = "Simple authority file is not valid."
        mess += " Here is the key value pair that is problematic: "
        mess += ",".join([str(check[1]), str(check[2])])
        raise ValueError(mess)
