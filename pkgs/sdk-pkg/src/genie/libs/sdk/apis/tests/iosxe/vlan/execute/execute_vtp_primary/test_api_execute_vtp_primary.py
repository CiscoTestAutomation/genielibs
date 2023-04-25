import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.execute import execute_vtp_primary


class TestExecuteVtpPrimary(unittest.TestCase):

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

    def test_execute_vtp_primary(self):
        result = execute_vtp_primary(self.device, 'mst')
        expected_output = ('System can become primary server for Mst feature only when configured as a '
 'server')
        self.assertEqual(result, expected_output)
