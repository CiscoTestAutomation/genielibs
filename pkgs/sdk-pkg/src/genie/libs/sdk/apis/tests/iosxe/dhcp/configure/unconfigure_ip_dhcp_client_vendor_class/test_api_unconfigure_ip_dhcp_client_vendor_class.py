from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_client_vendor_class


class TestUnconfigureIpDhcpClientVendorClass(TestCase):
    def test_unconfigure_ip_dhcp_client_vendor_class(self):
        self.device = Mock()
        unconfigure_ip_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'mac-address')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface GigabitEthernet0/0/1",
                    "no ip dhcp client vendor-class mac-address"],))

    def test_unconfigure_ip_dhcp_client_vendor_class_1(self):
        self.device = Mock()
        unconfigure_ip_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'disable')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface GigabitEthernet0/0/1",
                    "no ip dhcp client vendor-class disable"],))

    def test_unconfigure_ip_dhcp_client_vendor_class_2(self):
        self.device = Mock()
        unconfigure_ip_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'ascii')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface GigabitEthernet0/0/1",
                    "no ip dhcp client vendor-class ascii"],))

    def test_unconfigure_ip_dhcp_client_vendor_class_3(self):
        self.device = Mock()
        unconfigure_ip_dhcp_client_vendor_class(self.device, 'GigabitEthernet0/0/1', 'hex')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface GigabitEthernet0/0/1",
                    "no ip dhcp client vendor-class hex"],))
                

