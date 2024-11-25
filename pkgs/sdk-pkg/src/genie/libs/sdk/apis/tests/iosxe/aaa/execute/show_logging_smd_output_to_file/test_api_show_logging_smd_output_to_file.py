import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.execute import show_logging_smd_output_to_file


class TestShowLoggingSmdOutputToFile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_show_logging_smd_output_to_file(self):
        show_logging_smd_output_to_file(self.device, 'smd', 'vlan_id_attr_log.txt')
        self.assertIn(
            'show logging process smd start last clear to-file flash:vlan_id_attr_log.txt', 
            self.device.execute.call_args[0]
        )
