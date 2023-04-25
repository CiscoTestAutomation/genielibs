import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import request_platform_software_process_core


class TestRequestPlatformSoftwareProcessCore(unittest.TestCase):

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
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_request_platform_software_process_core(self):
        result = request_platform_software_process_core(self.device, 'host-manager', 'R0', '3', None)
        expected_output = ('$tform software process core host-manager switch 3 R0\r\n'
 'SUCCESS: Core file generated.')
        self.assertEqual(result, expected_output)
