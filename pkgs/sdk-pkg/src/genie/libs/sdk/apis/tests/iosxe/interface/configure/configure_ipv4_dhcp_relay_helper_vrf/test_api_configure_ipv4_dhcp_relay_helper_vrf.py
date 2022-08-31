import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ipv4_dhcp_relay_helper_vrf


class TestConfigureIpv4DhcpRelayHelperVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-P1C-PK:
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
        self.device = self.testbed.devices['Intrepid-P1C-PK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv4_dhcp_relay_helper_vrf(self):
        result = configure_ipv4_dhcp_relay_helper_vrf(self.device, 'Vlan100', '101.101.0.2', 'RAGUARD')
        expected_output = None
        self.assertEqual(result, expected_output)
