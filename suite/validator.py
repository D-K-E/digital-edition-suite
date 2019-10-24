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


def get_keys_array_from_object(obj: dict) -> dict:
    "get keys that are associated to objects from object"
    array_container = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            array_container[key] = value
    return array_container


def check_key_value_string(key: str, value: str):
    "validate key and value for string"
    if not isinstance(key, str):
        return False
    if not isinstance(value, str):
        return False
    if key.isdigit():
        return False
    return True


def check_key_value_string_object(obj: dict):
    """
    apply check key value string to object

    assumed structure
    {"my-key-string": "my value string"}
    """
    if not isinstance(obj, dict):
        return False
    for key, value in obj.items():
        if not check_key_value_string(key, value):
            return False
    return True


def check_key_value_int(key: str, value: str):
    "validate key and value for integer keys"
    if not isinstance(key, str):
        return False
    if not isinstance(value, str):
        return False
    if not key.isdigit():
        return False
    return True


def check_key_value_int_object(obj: dict):
    """
    apply check key value to int object

    assumed structure
    {"0": "my value string", "1": "my other string"}
    """
    if not isinstance(obj, dict):
        return False
    for key, value in obj.items():
        if not check_key_value_int(key, value):
            return False
    return True


def check_key_key_value_int_object(key: str, obj: dict) -> bool:
    """
    check key and value int object

    assumed structure
    {"my-string-key": {"0": "my value string", "1": "my other string"}}
    """
    if not isinstance(key, str):
        return False
    if not check_key_value_int_object(obj):
        return False
    return True


def check_key_key_value_string_object(key: str, obj: dict) -> bool:
    """
    check key and value string object

    assumed structure
    {"my-string-key": {"my-string-key-1": "my value string",
                       "my-string-key-2": "my other string"}}
    """
    if not isinstance(key, str):
        return False
    if not check_key_value_string_object(obj):
        return False
    return True


def validate_simple_authority_structure(author_file: dict) -> bool:
    """
    given a simple authority file output whether it is valid or not

    Simple Authority Spec
    ----------------------

    {"simple-no-1": {"some-value": "value definition"},
     "simple-no-n": {"some-value": "value definition"}
     }
    """
    assumed_structure = """
    {"simple-sample-word-1": {"lorem": ""},
     "simple-no-n": {"some-value": "value definition"}
     }
    """
    keys = set()
    for author_key, author_value in author_file.items():
        message = "Key value string object failed: {0}, {1}"
        message = message.format(author_key, str(author_value))
        if not check_key_key_value_string_object(author_key, author_value):
            return False, author_key, author_value, assumed_structure, message
        value_length = len(author_value)
        if value_length > 1:
            message = "author value must not have more than one key"
            message += " value pairs"
            return False, author_key, author_value, assumed_structure, message
        if author_key not in keys:
            keys.add(author_key)
        else:
            message = "Key: " + author_key + " exists in document"
            return False, author_key, author_value, assumed_structure, message
    return [True]


def validate_combined_authority_structure(author_file: dict) -> bool:
    """
    given a combined authority file output whether it is valid or not

    Combined Authority Spec
    ----------------------

    {
        "sample-combined-grammar-1": {
            "coordinating conjunction": "",
            "sample-relation-2": {"0": "sample-grammar-1"}
        },
        "sample-combined-grammar-2": {
            "feminine substantif": "",
            "sample-relation-2": {
                "0": "sample-grammar-6", "1": "sample-grammar-2"
            }
        }
    }
    """
    keys = set()
    assumed_structure = """
    {
        "sample-combined-grammar-1": {
            "coordinating conjunction": "",
            "sample-relation-2": {"0": "sample-grammar-1"}
        },
        "sample-combined-grammar-2": {
            "feminine substantif": "",
            "sample-relation-2": {
                "0": "sample-grammar-6", "1": "sample-grammar-2"
            }
        }
    }
    """
    for author_key, author_value in author_file.items():
        value_length = len(author_value)
        if value_length > 2:
            message = "author value must not have more than two keys"
            message += " value pairs"
            return False, author_key, author_value, assumed_structure, message
        if author_key not in keys:
            keys.add(author_key)
        else:
            message = "Key: " + author_key + " exists in document"
            return False, author_key, author_value, assumed_structure, message
        #
        for author_value_key, author_value_value in author_value.items():
            first_check = check_key_value_string(author_value_key,
                                                 author_value_value)
            second_check = check_key_key_value_int_object(author_value_key,
                                                          author_value_value)
            if not (first_check or second_check):
                #
                message = "Author value items: key: "
                message += str(author_value_key)
                message += ", value: " + str(author_value_value)
                message += "\nValue string check: " + str(first_check)
                message += "\nValue int object check: " + str(second_check)
                return (False, author_key,
                        author_value, assumed_structure, message)
        return [True]


def validate_entity_predicate_structure(predicate_file: dict) -> bool:
    """
    validate predicate, entity, and entity predicate link file structure

    assumed structure

    {   "entity/predicate-1": {"another-simple-id-no-0": {"0": "simple-id-no-1"}},
        "entity/predicate-2": {
            "another-simple/combined-id-no-0": {
                "0": "simple-id-no-2"
            }
        }
    }


    """
    assumed_structure = """
    {   "entity/predicate-1": {
            "another-simple/combined-id-no-0": {
                0: "simple/combined-id-no-1"
            }
        },
        "entity/predicate-2": {
            "another-simple/combined-id-no-0": {
                0: "simple/combined-id-no-2"
            }
        }
    }
    """
    keys = set()
    for predicate_key, predicate_value in predicate_file.items():
        if not isinstance(predicate_key, str):
            return False, predicate_key, predicate_value, assumed_structure
        for author_key, author_value_array in predicate_value.items():
            if not check_key_key_value_int_object(author_key,
                                                  author_value_array):
                return False, predicate_key, predicate_value, assumed_structure
        if predicate_key not in keys:
            keys.add(predicate_key)
        else:
            return False, predicate_key, predicate_value, assumed_structure
    return [True]


def check_structure_proc(checkfn: lambda x: x, filetype: str, params: dict):
    "Check structure for a given file using check function"
    check = checkfn(**params)
    if check[0] is False:
        mess = filetype + " file is not valid."
        mess += " Here is the key value pair that is problematic: "
        mess += ",".join([str(check[1]), str(check[2])])
        mess += ". See also the assumed file structure: " + check[3]
        raise ValueError(mess)


def check_simple_authority_structure(author_file: dict) -> None:
    "check simple authority file"
    check_structure_proc(params={"author_file": author_file},
                         checkfn=validate_simple_authority_structure,
                         filetype="Simple Authority")


def check_combined_authority_structure(author_file: dict) -> None:
    "check combined authority file"
    check_structure_proc(params={"author_file": author_file},
                         checkfn=validate_combined_authority_structure,
                         filetype="Combined Authority")


def check_predicate_file_structure(predicate_file: dict) -> None:
    "check predicate file structure"
    check_structure_proc(params={"predicate_file": predicate_file},
                         checkfn=validate_entity_predicate_structure,
                         filetype="Predicate Document")


def check_entity_file_structure(entity_file: dict) -> None:
    "check entity file structure"
    check_structure_proc(params={"predicate_file": entity_file},
                         checkfn=validate_entity_predicate_structure,
                         filetype="Entity Document")


def check_entity_predicate_link_file_structure(
        entity_predicate_link_file: dict) -> None:
    "check entity predicate link file structure"
    check_structure_proc(params={"predicate_file": entity_predicate_link_file},
                         checkfn=validate_entity_predicate_structure,
                         filetype="Entity Predicate Link Document")


def validate_combined_authority_content(author_file: dict,
                                        simple_ids: list) -> bool:
    "validate combined authority files using simple ids"
    assumed_structure = """
    {
        "combined-id-n": {
            "value": "value definition",
            "simple-id-no-1": {
                "0": "simple-no-0"
            }
        }
    }
    """
    for author_key, author_value in author_file.items():
        array_container = get_keys_array_from_object(author_value)
        for key, array_obj in array_container.items():
            if key not in simple_ids:
                message = "Key: " + key + " not in id list."
                return False, author_key, author_value, message
            for value in array_obj.values():
                if value not in simple_ids:
                    message = "Value: " + value + " not in id list "
                    return False, author_key, author_value, message
    return [True]


def validate_entity_predicate_content(entity_predicate_file: dict,
                                      simple_combined_ids: list) -> list:
    "validate predicate file content"
    assumed_structure = """
    {   "entity/predicate-1": {"another-simple-id-no-0": {"0": "simple-id-no-1"}},
        "entity/predicate-2": {
            "another-simple/combined-id-no-0": {
                "0": "simple-id-no-2"
            }
        },
    "entity/predicate-3": {
            "another-simple/combined-id-no-0": {
                "0": "entity/predicate-id-no-2"
            }
        }
    }
    """
    keys = list(entity_predicate_file.keys())
    for predicate_key, predicate_value in entity_predicate_file.items():
        for key, array_obj in predicate_value.items():
            if key not in simple_combined_ids:
                message = "Key: " + key + " not in id list."
                return False, predicate_key, predicate_value, message
            for value in array_obj.values():
                first_check = value not in simple_combined_ids
                second_check = value not in keys
                cond = first_check and second_check
                if cond:
                    message = "Value: " + value + ""
                    message += "\nCondition: " + str(cond)
                    message += "\nValue not in ids: " + str(first_check)
                    message += "\nValue not in keys: " + str(second_check)
                    return False, predicate_key, predicate_value, message
    return [True]


def validate_entity_predicate_link_content(link_file: dict,
                                           simple_combined_ids: list,
                                           predicate_ids: list) -> list:
    "validate entity predicate link file content"
    for entity_id, link_values in link_file.items():
        for authority_id, predicates in link_values.items():
            if authority_id not in simple_combined_ids:
                message = "Authority id: " + authority_id + " not in id list."
                return False, entity_id, link_values, message
            for predicate in predicates.values():
                if predicate not in predicate_ids:
                    message = "Predicate value: " + predicate
                    message += " not in available predicate ids"
                    return False, entity_id, link_values, message
    return [True]


def check_content_proc(checkfn: lambda x: x,
                       filetype: str, params: dict):
    "Check content for a given file type"
    check = checkfn(**params)
    if check[0] is False:
        mess = filetype + " file is not valid."
        mess += "\nHere is the key value pair that is problematic: "
        mess += ",".join([str(check[1]), str(check[2])])
        mess += ".\nSee also the assumed file structure: " + check[3]
        mess += "\nSee the message of validation function: " + check[4]
        raise ValueError(mess)
