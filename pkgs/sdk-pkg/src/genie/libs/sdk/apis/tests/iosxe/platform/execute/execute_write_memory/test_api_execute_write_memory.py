import unittest
from unittest.mock import Mock, ANY
from genie.libs.sdk.apis.iosxe.platform.execute import execute_write_memory


class TestExecuteWriteMemory(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_execute_write_memory(self):
        self.device.execute = Mock(return_value=['[OK]'])
        execute_write_memory(self.device)
        self.device.execute.assert_called_with('write memory', reply=ANY, timeout=300)
