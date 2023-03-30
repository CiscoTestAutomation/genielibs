import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform_licensing.execute import execute_license_smart_save_usage_all_file


class TestExecuteLicenseSmartSaveUsageAllFile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_license_smart_save_usage_all_file(self):
        result = execute_license_smart_save_usage_all_file(self.device, 'bootflash:test.txt')
        expected_output = None
        self.assertEqual(result, expected_output)
