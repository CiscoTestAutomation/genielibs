import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import request_system_shell


class TestRequestSystemShell(unittest.TestCase):

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

    def test_request_system_shell(self):
        result = request_system_shell(self.device, 'active', 'R0', False, False, None)
        expected_output = ('Activity within this shell can jeopardize the functioning of the system.\r\n'
 'Are you sure you want to continue? [y/n]')
        self.assertEqual(result, expected_output)
