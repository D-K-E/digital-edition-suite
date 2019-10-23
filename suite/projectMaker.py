# author: Kaan Eraslan
# license: see, LICENSE
# purpose: set up a project directory for digital publishing and conservation
# project

import os
import json
import argparse


def assert_first_not_second_proc(path1: str, path2: str) -> None:
    "assert first path as true and second not true with isdir"
    assert os.path.isdir(path1)
    assert not os.path.isdir(path2)


def write_to_json(path: str, obj: dict) -> None:
    "write object to path as json"
    with open(path, "w", encoding="utf-8") as fd:
        json.dump(obj, fd, ensure_ascii=False, indent=2)
    return


def mk_project_dir(mainpath: str, project_name: str) -> str:
    "make project directory in given main path"
    project_path = os.path.join(mainpath, project_name)
    assert_first_not_second_proc(mainpath, project_path)
    os.mkdir(project_path)
    return project_path


def mk_project_assets(project_path: str) -> str:
    "make assets directory in project"
    asset_path = os.path.join(project_path, "assets")
    assert_first_not_second_proc(project_path, asset_path)
    os.mkdir(asset_path)
    return asset_path


def mk_project_predicate(asset_path: str) -> str:
    "make predicate directory in project assets"
    predicate_path = os.path.join(asset_path, "predicate")
    assert_first_not_second_proc(asset_path, predicate_path)
    os.mkdir(predicate_path)
    return predicate_path


def mk_project_link(asset_path: str) -> str:
    "make predicate directory in project assets"
    link_path = os.path.join(asset_path, "link")
    assert_first_not_second_proc(asset_path, link_path)
    os.mkdir(link_path)
    return link_path


def mk_project_entity(asset_path: str) -> str:
    "make entity directory in project assets"
    entity_path = os.path.join(asset_path, "entity")
    assert_first_not_second_proc(asset_path, entity_path)
    os.mkdir(entity_path)
    return entity_path


def mk_project_authority(predicate_path: str) -> str:
    "make authority directory in project assets"
    author_dir = os.path.join(predicate_path, "authority")
    assert_first_not_second_proc(predicate_path, author_dir)
    os.mkdir(author_dir)
    return author_dir


def mk_simple_authority(author_dir: str) -> str:
    "make simple authority directory in project authority directory"
    simple_dir = os.path.join(author_dir, "simple")
    assert_first_not_second_proc(author_dir, simple_dir)
    os.mkdir(simple_dir)
    return simple_dir


def mk_project_dirs(mainpath: str, project_name: str):
    "make project directories"
    project_dir = mk_project_dir(mainpath, project_name)
    asset_dir = mk_project_assets(project_dir)
    predicate_dir = mk_project_predicate(asset_dir)
    link_dir = mk_project_link(asset_dir)
    entity_dir = mk_project_entity(asset_dir)
    author_dir = mk_project_authority(predicate_dir)
    simple_dir = mk_simple_authority(author_dir)
    return simple_dir, author_dir, entity_dir, link_dir, predicate_dir


def mk_sample_document(parent_path: str,
                       doc_name: str, sample_doc: dict) -> None:
    "make sample document given parent path and its name with its structure"
    assert os.path.isdir(parent_path)
    doc_path = os.path.join(parent_path, doc_name)
    write_to_json(doc_path, sample_doc)


def mk_sample_simple_authority(simple_dir: str) -> None:
    "make a sample simple authority document"
    sample_doc = {
        "sample-word-1": {"lorem": ""},
        "sample-word-2": {"ipsum": ""},
        "sample-word-3": {"dolor": ""},
        "sample-word-4": {"sit": ""},
        "sample-word-5": {"amet": ""},
        "sample-simple-n": {"value": "value definition"}
    }
    mk_sample_document(simple_dir, "sampleSimple.json", sample_doc)


def mk_sample_combined_authority(author_dir: str) -> None:
    "make a sample combined authority document"
    sample_doc = {
        "sample-combined-grammar-1": {
            "coordinating conjunction": "",
            "sample-relation-2": {"0": "sample-grammar-1"}
        },
        "sample-combined-grammar-2": {
            "feminine substantif": "",
            "sample-relation-2": {
                "0": "sample-grammar-6", "1": "sample-grammar-2"
            }
        },
        "sample-combined-n": {
            "value": "value definition",
            "sample-relation-n": {
                "0": "sample-simple-id",
                "1": "sample-simple-id-n"
            }
        }
    }
    mk_sample_document(author_dir, "sampleCombinedSimple.json", sample_doc)


def mk_sample_predicate(asset_path: str) -> None:
    "make sample predicate document"
    sample_doc = {
        "sample-predicate-1": {
            "sample-relation-3": {
                "0": "sample-combined-grammar-2",
                "1": "sample-grammar-5",
                "2": "sample-grammar-7",
            },
            "sample-relation-1": {"0": "sample-word-3"}
        }
    }
    mk_sample_document(asset_path, "samplePredicate.json", sample_doc)


def mk_sample_entity_relation(asset_path: str) -> None:
    "make sample entity relations document"
    sample_doc = {
        "sample-entity-1": {
            "sample-relation-1": {"0": "sample-word-2"}
        },
        "sample-entity-2": {
            "sample-relation-2": {"0": "sample-entity-1"}
        }
    }
    mk_sample_document(asset_path, "sampleEntityRelations.json", sample_doc)


def mk_sample_entity_predicate_link(asset_path: str) -> None:
    "make sample entity predicate link document"
    sample_doc = {
        "sample-entity-1": {
            "sample-relation-3": {"0": "sample-predicate-1"}
        },
        "sample-entity-2": {
            "sample-relation-3": {"0": "sample-predicate-2"}
        }
    }
    mk_sample_document(
        asset_path, "sampleEntityPredicateLink.json", sample_doc)


def make_samples_proc(simple_dir, author_dir,
                      predicate_dir, entity_dir, link_dir):
    "make samples procedure"
    mk_sample_simple_authority(simple_dir)
    mk_sample_combined_authority(author_dir)
    mk_sample_predicate(predicate_dir)
    mk_sample_entity_relation(entity_dir)
    mk_sample_entity_predicate_link(link_dir)


if __name__ == "__main__":
    main_path = input("enter parent directory for project: ")
    project_name = input("Enter a project name: ")
    main_dir = os.path.abspath(main_path)
    (simple_dir, author_dir,
     entity_dir, link_dir, predicate_dir) = mk_project_dirs(main_dir,
                                                            project_name)
    make_samples_proc(simple_dir, author_dir, predicate_dir, entity_dir,
                      link_dir)
    print("project structure done")
