from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_client_vendor_class
from unittest.mock import Mock

class TestUnconfigureIpv6DhcpClientVendorClass(TestCase):

    def test_unconfigure_ipv6_dhcp_client_vendor_class(self):
        self.device = Mock()
        unconfigure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'mac-address')
        self.device.configure.assert_called_with(['interface GigabitEthernet0/0/1', 'no ipv6 dhcp client vendor-class mac-address'])

    def test_unconfigure_ipv6_dhcp_client_vendor_class_1(self):
        self.device = Mock()
        unconfigure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'disable')
        self.device.configure.assert_called_with(['interface GigabitEthernet0/0/1', 'no ipv6 dhcp client vendor-class disable'])
        

    def test_unconfigure_ipv6_dhcp_client_vendor_class_2(self):
        self.device = Mock()
        unconfigure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'ascii')
        self.device.configure.assert_called_with(['interface GigabitEthernet0/0/1', 'no ipv6 dhcp client vendor-class ascii'])
        

    def test_unconfigure_ipv6_dhcp_client_vendor_class_3(self):
        self.device = Mock()
        unconfigure_ipv6_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'hex')
        self.device.configure.assert_called_with(['interface GigabitEthernet0/0/1', 'no ipv6 dhcp client vendor-class hex'])
        
        