# author: Kaan Eraslan
# license: see, LICENSE
# purpose: test scripts of suite

import unittest

from suite import idchecker as idc
from suite import projectMaker as pjm
from suite import validator as vd

import os
import json
import shutil


class TestDigitalEditionSuite(unittest.TestCase):
    "test edition"

    def setUp(self):
        "set up"
        self.currentdir = os.path.abspath(os.curdir)
        self.testdir = os.path.join(self.currentdir, "tests")
        self.assetdir = os.path.join(self.testdir, "assets")
        self.project_parent = os.path.join(self.testdir, "sampleProjectParent")
        self.project_name = "sampleProject"
        self.project_path = os.path.join(self.project_parent,
                                         self.project_name)
        self.simple_doc1_path = os.path.join(self.assetdir, "simple1.json")
        self.simple_doc2_path = os.path.join(self.assetdir, "simple2.json")
        self.simple_doc3_path = os.path.join(self.assetdir, "simple3.json")
        self.combined_doc_path = os.path.join(self.assetdir, "combined1.json")
        self.predicate_doc_path = os.path.join(
            self.assetdir, "predicate1.json")
        self.entity_doc_path = os.path.join(self.assetdir, "entity1.json")
        self.link_doc_path = os.path.join(self.assetdir, "link1.json")

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

    def test_read_json(self):
        "test read json"
        (simple_dir, author_dir,
         entity_dir, link_dir, predicate_dir) = pjm.mk_project_dirs(
            self.project_parent,
            self.project_name)
        pjm.make_samples_proc(simple_dir, author_dir,
                              predicate_dir, entity_dir, link_dir)
        link_path = os.path.join(link_dir, "sampleEntityPredicateLink.json")
        cmp_link = {
            "sample-entity-1": {
                "sample-relation-3": {"0": "sample-predicate-1"}
            },
            "sample-entity-2": {
                "sample-relation-3": {"0": "sample-predicate-2"}
            }
        }
        link_doc = vd.read_json(link_path)
        self.assertEqual(cmp_link, link_doc)
        shutil.rmtree(self.project_path)

    def test_get_keys_array_from_object(self):
        ""
        array_obj = {"myval": "another value",
                     "my1": {"0": "sample-1", "1": "sample-2"},
                     "my2": {"0": "sample-3", "1": "sample-6"},
                     "my3": {"0": "sample-7", "1": "sample-2", "2": "sample-9"}
                     }
        cmp_obj = {"my1": {"0": "sample-1", "1": "sample-2"},
                   "my2": {"0": "sample-3", "1": "sample-6"},
                   "my3": {"0": "sample-7", "1": "sample-2", "2": "sample-9"}
                   }
        array_obj = vd.get_keys_array_from_object(array_obj)
        self.assertEqual(array_obj, cmp_obj)

    def test_check_key_value_string(self):
        ""
        self.assertEqual(True,
                         vd.check_key_value_string("my1", "value"))
        self.assertEqual(False,
                         vd.check_key_value_string(0, "value"))

    def test_key_value_string_object(self):
        ""
        testobj1 = {"my": "sample-7", "string": "sample-2", "key": "sample-9"}
        testobj2 = {"0": "sample-7", "1": "sample-2", "2": "sample-9"}
        testobj3 = {0: "sample-7", 1: "sample-2", "2": "sample-9"}
        self.assertEqual(True, vd.check_key_value_string_object(testobj1))
        self.assertEqual(False, vd.check_key_value_string_object(testobj2))
        self.assertEqual(False, vd.check_key_value_string_object(testobj3))

    def test_check_key_value_int(self):
        ""
        self.assertEqual(True,
                         vd.check_key_value_int("0", "value"))
        self.assertEqual(False,
                         vd.check_key_value_int(0, "value"))
        self.assertEqual(False,
                         vd.check_key_value_int("mykey", "value"))
        self.assertEqual(False,
                         vd.check_key_value_int("0", 25))

    def test_check_key_value_int_object(self):
        ""
        test_obj1 = {"0": "sample-1", "1": "sample-2", "3": "sample-9"}
        test_obj2 = {"for": "sample-1", "1": "sample-2", "3": "sample-9"}
        self.assertEqual(True, vd.check_key_value_int_object(test_obj1))
        self.assertEqual(False, vd.check_key_value_int_object(test_obj2))

    def test_check_key_key_value_int_object(self):
        ""
        test_obj1 = {
            "my3": {"0": "sample-7", "1": "sample-2", "2": "sample-9"}
        }
        test_obj2 = {
            "my2": {"for": "sample-3", "1": "sample-6"},
        }
        for key, val in test_obj1.items():
            self.assertEqual(True,
                             vd.check_key_key_value_int_object(key, val))
        for key, val in test_obj2.items():
            self.assertEqual(False,
                             vd.check_key_key_value_int_object(key, val))

    def test_check_key_key_value_string_object(self):
        ""
        test_obj1 = {
            "my3": {"my": "sample-7", "key": "sample-2", "here": "sample-9"}
        }
        test_obj2 = {
            "my2": {0: "sample-3", "1": "sample-6"},
        }
        test_obj3 = {
            "my2": {"0": "sample-3", "1": "sample-6"},
        }
        for key, val in test_obj1.items():
            self.assertEqual(True,
                             vd.check_key_key_value_string_object(key, val))
        #
        for key, val in test_obj2.items():
            self.assertEqual(False,
                             vd.check_key_key_value_string_object(key, val))
        #
        for key, val in test_obj3.items():
            self.assertEqual(False,
                             vd.check_key_key_value_string_object(key, val))
        #

    def test_validate_simple_authority_structure(self):
        ""
        doc1 = vd.read_json(self.simple_doc1_path)
        doc2 = vd.read_json(self.simple_doc2_path)
        doc3 = vd.read_json(self.simple_doc3_path)
        check1 = vd.validate_simple_authority_structure(doc1)
        check2 = vd.validate_simple_authority_structure(doc2)
        check3 = vd.validate_simple_authority_structure(doc3)
        self.assertEqual(check1[0], True)
        self.assertEqual(check2[0], True)
        self.assertEqual(check3[0], True)

    def test_validate_combined_authority_structure(self):
        ""
        doc1 = vd.read_json(self.combined_doc_path)
        check = vd.validate_combined_authority_structure(doc1)
        self.assertEqual(check[0], True)

    def test_validate_predicate_entity_link_structure(self):
        ""
        doc1 = vd.read_json(self.predicate_doc_path)
        doc2 = vd.read_json(self.entity_doc_path)
        doc3 = vd.read_json(self.link_doc_path)
        check1 = vd.validate_entity_predicate_structure(doc1)
        check2 = vd.validate_entity_predicate_structure(doc2)
        check3 = vd.validate_entity_predicate_structure(doc3)
        self.assertEqual(check1[0], True)
        self.assertEqual(check2[0], True)
        self.assertEqual(check3[0], True)


if __name__ == "__main__":
    unittest.main()
