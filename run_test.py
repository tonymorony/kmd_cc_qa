#!/usr/bin/env python3.6
import unittest

from test_modules import get_tokens_list
from test_modules import create_token

class TestCases(unittest.TestCase):
    def test_add_token(self):
        self.assertEqual(create_token("BRK","TEST1","0.1","AUTO-TEST"), True)

if __name__ == '__main__':
    unittest.main()
