import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server


class TestConfigureRadiusServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          n08HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['n08HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_radius_server(self):
        result = configure_radius_server(self.device, {'acct_port': '1813',
 'auth_port': '1812',
 'ipv4': '20.20.20.2',
 'key': 'Cisco',
 'server_name': 'ISE2.7'})
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_radius_server_1(self):
        result = configure_radius_server(self.device, {'acct_port': '1813',
 'auth_port': '1812',
 'dscp_acct': '10',
 'dscp_auth': '20',
 'ipv4': '20.20.20.2',
 'key': 'Cisco',
 'server_name': 'ISE2.7'})
        expected_output = None
        self.assertEqual(result, expected_output)
