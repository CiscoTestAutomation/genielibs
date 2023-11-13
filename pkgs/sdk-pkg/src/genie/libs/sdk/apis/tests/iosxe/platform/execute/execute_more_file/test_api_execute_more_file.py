import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_more_file


class TestExecuteMoreFile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Sanity-ASR2X:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Sanity-ASR2X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_more_file(self):
        result = execute_more_file(self.device, 'bootflash:core/Sanity-ASR2X_RP_0-system-report_20230912-151005-UTC-info.txt', 'ucode')
        expected_output = '/harddisk/core/Sanity-ASR2X_RP_0_cpp-mcplo-ucode_20230912-150929-UTC.core.gz'
        self.assertEqual(result, expected_output)
