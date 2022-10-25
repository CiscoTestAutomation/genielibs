import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_client_vendor_class


class TestConfigureIpv6DhcpClientVendorClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Fei-Elixir2:
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
        self.device = self.testbed.devices['Fei-Elixir2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_dhcp_client_vendor_class(self):
        result = configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'mac-address', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ipv6_dhcp_client_vendor_class_1(self):
        result = configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'disable', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ipv6_dhcp_client_vendor_class_2(self):
        result = configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'ascii', 'abcDEF123')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ipv6_dhcp_client_vendor_class_3(self):
        result = configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'hex', '0102030a0b0c')
        expected_output = None
        self.assertEqual(result, expected_output)
