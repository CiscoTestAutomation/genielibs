import unittest
from unittest.mock import Mock

from pyats.topology import loader
from genie.libs.sdk.apis.execute import execute_copy_run_to_start


class TestExecuteCopyRunToStart(unittest.TestCase):

  def setUp(self):
    self.device = Mock()

  def test_execute_copy_run_to_start(self):
    self.device.execute = Mock(return_value="Copy completed successfully")
    result = execute_copy_run_to_start(self.device, 60, 30, 10, False)
    expected_output = True
    self.assertEqual(result, expected_output)

  def test_execute_copy_run_to_start_fail(self):
    self.device.execute = Mock(return_value="Copy failed due to error")
    result = execute_copy_run_to_start(self.device, 60, 30, 10, False)
    expected_output = None
    self.assertEqual(result, expected_output)
