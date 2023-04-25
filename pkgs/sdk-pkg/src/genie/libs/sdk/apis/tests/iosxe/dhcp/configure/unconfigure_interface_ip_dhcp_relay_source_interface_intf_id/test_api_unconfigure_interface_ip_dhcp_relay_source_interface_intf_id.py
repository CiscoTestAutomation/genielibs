import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_dhcp_relay_source_interface_intf_id


class TestUnconfigureInterfaceIpDhcpRelaySourceInterfaceIntfId(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Cat9300_VTEP1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9300_VTEP1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_interface_ip_dhcp_relay_source_interface_intf_id(self):
        result = unconfigure_interface_ip_dhcp_relay_source_interface_intf_id(self.device, 'vlan100', 'Loopback1')
        expected_output = None
        self.assertEqual(result, expected_output)
