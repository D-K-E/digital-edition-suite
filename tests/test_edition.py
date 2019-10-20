# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest

from suite import idchecker as idc
from suite import projectMaker as pjm
from suite import validator as vd

import os
import shutil


class TestDigitalEditionSuite(unittest.TestCase):
    "test edition"

    def setUp(self):
        "set up"
        self.currentdir = os.path.abspath(os.curdir)
        self.testdir = os.path.join(self.currentdir, "tests")
        self.project_parent = os.path.join(self.testdir, "sampleProjectParent")
        self.project_name = "sampleProject"
        self.project_path = os.path.join(self.project_parent,
                                         self.project_name)
        self.simple_doc1 = """
        {
            "sample-word-1": {"lorem": ""},
            "sample-word-2": {"ipsum": ""},
            "sample-word-3": {"dolor": ""},
            "sample-word-4": {"sit": ""},
            "sample-word-5": {"amet": ""},
        }
        """
        self.simple_doc2 = """
        {
            "sample-grammar-1": {"conjunction": ""},
            "sample-grammar-2": {"substantif": ""},
            "sample-grammar-3": {"verb": ""},
            "sample-grammar-4": {"subject": ""},
            "sample-grammar-5": {"nominative": ""},
            "sample-grammar-6": {"feminine": ""},
        }
        """
        self.simple_doc3 = """
        {
            "sample-relation-1": {"equals": ""},
            "sample-relation-2": {"contains": ""},
            "sample-relation-3": {"defined as": ""},
        }
        """
        self.combined_doc = """
        {
            "sample-combined-grammar-1": {
                "coordinating conjunction": "",
                "contains": {0: "sample-grammar-1"}
            },
            "sample-combined-grammar-2": {
                "feminine substantif": "",
                "contains": {0: "sample-grammar-6", 1: "sample-grammar-2"}
            }
        }
        """
        self.predicate_doc = """
        {
            "sample-predicate-1": {
                "sample-relation-1": {
                    0: "",
                    1: "",
                    2: "",
                }
            }
        }
        """

    def test_assert_first_not_second_proc(self):
        ""
        noneval = pjm.assert_first_not_second_proc(self.project_parent,
                                                   self.project_path)
        self.assertEqual(noneval, None)

    def test_make_project_dirs(self):
        "test make project dirs"
        asset_dir_cmp = os.path.join(self.project_path, "assets")
        predicate_dir_cmp = os.path.join(asset_dir_cmp, "predicate")
        link_dir_cmp = os.path.join(asset_dir_cmp, "link")
        entity_dir_cmp = os.path.join(asset_dir_cmp, "entity")
        authority_dir_cmp = os.path.join(predicate_dir_cmp, "authority")
        simple_dir_cmp = os.path.join(authority_dir_cmp, "simple")
        (simple_dir, author_dir,
         entity_dir, link_dir, predicate_dir) = pjm.mk_project_dirs(
            self.project_parent,
            self.project_name)
        self.assertEqual(entity_dir_cmp, entity_dir)
        self.assertEqual(author_dir, authority_dir_cmp)
        self.assertEqual(simple_dir, simple_dir_cmp)
        self.assertEqual(link_dir, link_dir_cmp)
        self.assertEqual(predicate_dir_cmp, predicate_dir)
        cond = bool(os.path.isdir(entity_dir) and
                    os.path.isdir(author_dir) and
                    os.path.isdir(link_dir) and
                    os.path.isdir(simple_dir) and
                    os.path.isdir(predicate_dir))
        self.assertTrue(cond)
        shutil.rmtree(self.project_path)

    def test_make_sample_files(self):
        "make sample files"
        (simple_dir, author_dir,
         entity_dir, link_dir, predicate_dir) = pjm.mk_project_dirs(
            self.project_parent,
            self.project_name)
        pjm.make_samples_proc(simple_dir, author_dir,
                              predicate_dir, entity_dir, link_dir)
        link_path = os.path.join(link_dir, "sampleEntityPredicateLink.json")
        entity_path = os.path.join(entity_dir, "sampleEntityRelations.json")
        predicate_path = os.path.join(predicate_dir, "samplePredicate.json")
        author_path = os.path.join(author_dir, "sampleCombinedSimple.json")
        simple_path = os.path.join(simple_dir, "sampleSimple.json")
        cond = bool(os.path.isfile(simple_path) and
                    os.path.isfile(author_path) and
                    os.path.isfile(predicate_path) and
                    os.path.isfile(entity_path) and
                    os.path.isfile(link_path))
        self.assertTrue(cond)
        shutil.rmtree(self.project_path)


if __name__ == "__main__":
    unittest.main()
