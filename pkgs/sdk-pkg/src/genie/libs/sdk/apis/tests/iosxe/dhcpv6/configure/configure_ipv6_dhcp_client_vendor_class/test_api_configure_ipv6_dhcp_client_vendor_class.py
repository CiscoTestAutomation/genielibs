from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_client_vendor_class
from unittest.mock import Mock

class TestConfigureIpv6DhcpClientVendorClass(TestCase):

    def test_configure_ipv6_dhcp_client_vendor_class(self):
        self.device = Mock()
        configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'mac-address', None)
        self.assertEqual(self.device.configure.mock_calls[0].args, (['interface GigabitEthernet0/0/1', 'ipv6 dhcp client vendor-class mac-address'],))

    def test_configure_ipv6_dhcp_client_vendor_class_1(self):
        self.device = Mock()
        configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'disable', None)
        self.assertEqual(self.device.configure.mock_calls[0].args, (['interface GigabitEthernet0/0/1', 'ipv6 dhcp client vendor-class disable'],))

    def test_configure_ipv6_dhcp_client_vendor_class_2(self):
        self.device = Mock()
        configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'ascii', 'abcDEF123')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['interface GigabitEthernet0/0/1', 'ipv6 dhcp client vendor-class ascii abcDEF123'],))
        
    def test_configure_ipv6_dhcp_client_vendor_class_3(self):
        self.device = Mock()
        configure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'hex', '0102030a0b0c')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['interface GigabitEthernet0/0/1', 'ipv6 dhcp client vendor-class hex 0102030a0b0c'],))
