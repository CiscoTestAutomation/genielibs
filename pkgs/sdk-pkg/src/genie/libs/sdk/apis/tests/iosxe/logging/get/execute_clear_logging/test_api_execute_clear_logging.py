import os
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.logging.get import execute_clear_logging
from unittest.mock import Mock
class TestExecuteClearLogging(TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_execute_clear_logging(self):
        result = execute_clear_logging(self.device)
        self.assertIn(
            'clear logging',
            self.device.execute.call_args_list[0][0]
        )
