import unittest
from genie.libs.sdk.genie_yamls import datafile


class TestGenieYamls(unittest.TestCase):

    def test_genie_yamls(self):
        for mode in ['trigger', 'verification', 'subsection', 'pts', 'health']:
            df = datafile(mode)
            self.assertIn(mode, df)

    def test_genie_yamls_invalid(self):
        with self.assertRaises(Exception):
            datafile('invalid')
