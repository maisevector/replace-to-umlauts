#!/usr/bin/env python3
"""
This module contains the tests for replace-to-umlauts
"""

import unittest
import os.path
import json
import replace_to_umlauts as rtu

TEST_PATH_DICT='test_path.json'

class TestDictCreation(unittest.TestCase):
    """
    Tests for the creation of the dictionary.
    """
    def test_dict_creation(self):
        """
        Create the dictionary on some local path.
        """
        rtu.create_dict(TEST_PATH_DICT)
        self.assertTrue(os.path.exists(TEST_PATH_DICT))

class TestProcessing(unittest.TestCase):
    """
    Tests for the correct word processing.
    """
    def test_words(self):
        """
        Test some words
        """
        test_str = ["Aeon", "Oese", "Uebelkeit", "aendern", "moeglich", "Hueter", "Gruesse",
                    "Floss", "Israeli", "Oboe", "Reue"]
        res_str = ["Äon", "Öse", "Übelkeit", "ändern", "möglich", "Hüter", "Grüße",
                   "Floß", "Israeli", "Oboe", "Reue"]
        with open(os.path.expanduser(TEST_PATH_DICT),"r",encoding="utf8") as read_file:
            ngerman_dict = json.load(read_file)
        for word,testword in zip(test_str,res_str):
            self.assertEqual(rtu.replace_word(word,ngerman_dict), testword)
