# author: Kaan Eraslan
# license: see, LICENSE
# purpose: check ids for given project assets
# no duplicate should be involved in any of the keys

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


def check_for_json(idstr: str, jsonpath: dict):
    "Check whether given id string is contained in given json object"
    return idstr in read_json(jsonpath)


def build_project_structure(project_path: str):
    "given project path build project structure for easy acces to locations"
    structure = {}
    assetdir = os.path.join(project_path, "assets")
    predicate_dir = os.path.join(assetdir, "predicate")
    link_dir = os.path.join(assetdir, "link")
    entity_dir = os.path.join(assetdir, "entity")
    author_dir = os.path.join(predicate_dir, "authority")
    simple_dir = os.path.join(author_dir, "simple")
    structure["link"] = link_dir
    structure["entity"] = entity_dir
    structure["predicate"] = predicate_dir
    structure["author"] = author_dir
    structure["simple"] = simple_dir
    return structure


def check_id_in_project(project_path: str, idstr: str) -> bool:
    "check id string in project"
    structure = build_project_structure(project_path)
    for asset_type, asset_path in structure.items():
        jsonglob = os.path.join(asset_path, "*.json")
        jsonfiles = glob.glob(jsonglob)
        for jsonpath in jsonfiles:
            if check_for_json(idstr, jsonpath):
                return True, asset_type, jsonpath
    return [False]


if __name__ == "__main__":
    project_path = input("Enter project path: ")
    idstr = input("Enter id string: ")
    check = check_id_in_project(project_path, idstr)
    if check[0] is False:
        print("id string:",
              idstr, "is usable.")
        sys.exit(0)
    #
    print("id string:", idstr,
          "has a duplicate in the asset type", check[1],
          "at", check[2])
    print("Duplicate ids are not allowed, please enter another id string")
    sys.exit(0)
