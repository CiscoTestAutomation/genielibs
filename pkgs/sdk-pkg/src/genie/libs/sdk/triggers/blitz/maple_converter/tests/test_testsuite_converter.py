#! /usr/bin/env python
import os
import sys
import tempfile
import unittest
import ruamel.yaml

from unittest.mock import Mock
from unittest.mock import patch

from genie.libs.sdk.triggers.blitz.maple_converter.maple_converter import Converter
from genie.libs.sdk.triggers.blitz.maple_converter.testsuite_converter import Testsuite_Converter

from pyats.easypy.job import Job
from pyats.easypy import runtime
from pyats.easypy.tests.common_funcs import init_runtime

def check_maple_env():
   if not os.environ.get('MAPLE_PATH'):
      return True
   
   if not os.path.isdir(os.path.join(os.getcwd(),
                        'genie/libs/sdk/triggers/blitz/tests/mock_yamls')):
      return True

   return False

class TestSuiteConverter(unittest.TestCase):

   def setUp(self):

      test_dir_path = os.path.abspath(
                                 os.path.join(os.path.dirname( __file__ ), '../..', 'tests'))
      self.testsuite = os.path.join(test_dir_path, 'mock_yamls/maple_testsuite.yaml')
      self.converter = Testsuite_Converter(self.testsuite)

      file_path = os.path.dirname(os.path.abspath(__file__))
      f, self.jobfile = tempfile.mkstemp()
      init_runtime(runtime)
      runtime.configuration.load()
      runtime.job = Job(jobfile = self.jobfile,
                        runtime = runtime,
                        **runtime.configuration.components.job)

   
   @unittest.skipIf(check_maple_env(), "MAPLE_PATH is not set")
   def test_grun_kwargs_generator(self):

      with patch("genie.libs.sdk.triggers.blitz.maple_converter"
                 ".maple_converter.Converter.convert", return_value=['test1', 'test2']) as func:
         grun_kwargs = list(self.converter.grun_kwargs_generator())
         func.assert_called()

      print('aa')

if __name__ == '__main__':
    unittest.main()