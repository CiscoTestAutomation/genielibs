import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ipv4_dhcp_relay_helper


class TestUnconfigureIpv4DhcpRelayHelper(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          FE2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['FE2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ipv4_dhcp_relay_helper(self):
        result = unconfigure_ipv4_dhcp_relay_helper(self.device, 'Vlan110', '4.4.4.4')
        expected_output = None
        self.assertEqual(result, expected_output)
