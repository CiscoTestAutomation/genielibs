import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_pool


class TestUnconfigureDhcpPool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500L
            type: c9500L
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_dhcp_pool(self):
        result = unconfigure_dhcp_pool(self.device, 'evpn_pool', 'None', '192.168.1.0', '255.255.255.0', 'green', '192.168.1.200')
        expected_output = None
        self.assertEqual(result, expected_output)
