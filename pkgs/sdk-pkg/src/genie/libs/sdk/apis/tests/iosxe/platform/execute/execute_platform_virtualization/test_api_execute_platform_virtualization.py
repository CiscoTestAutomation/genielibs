import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_platform_virtualization


class TestExecutePlatformVirtualization(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Sanity-ASR9X:
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
        self.device = self.testbed.devices['Sanity-ASR9X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_platform_virtualization(self):
        result = execute_platform_virtualization(self.device, 'RP', 'active')
        expected_output = ' Rom-monitor variable ENABLE_VTX has already been set.'
        self.assertEqual(result, expected_output)
