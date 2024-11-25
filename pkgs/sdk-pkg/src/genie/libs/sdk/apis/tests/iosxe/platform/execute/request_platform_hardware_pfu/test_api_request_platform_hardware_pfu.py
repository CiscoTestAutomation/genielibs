import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import request_platform_hardware_pfu


class TestRequestPlatformHardwarePfu(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SA-C9350-24P:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SA-C9350-24P']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_request_platform_hardware_pfu(self):
        result = request_platform_hardware_pfu(self.device, '1', 'R0', 2, 'off')
        expected_output = None
        self.assertEqual(result, expected_output)
