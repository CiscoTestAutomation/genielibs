import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.execute import execute_clear_aaa_counters_server


class TestExecuteClearAaaCountersServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_execute_clear_aaa_counters_server(self):
        execute_clear_aaa_counters_server(self.device)
        self.assertIn(
            'clear aaa counters servers  all',
            self.device.execute.call_args[0])