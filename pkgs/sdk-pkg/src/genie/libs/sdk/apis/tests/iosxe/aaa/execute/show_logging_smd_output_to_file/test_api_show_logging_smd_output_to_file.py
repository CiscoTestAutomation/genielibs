import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.execute import show_logging_smd_output_to_file


class TestShowLoggingSmdOutputToFile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          VCR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_show_logging_smd_output_to_file(self):
        result = show_logging_smd_output_to_file(self.device, 'smd', 'vlan_id_attr_log.txt')
        expected_output = None
        self.assertEqual(result, expected_output)
