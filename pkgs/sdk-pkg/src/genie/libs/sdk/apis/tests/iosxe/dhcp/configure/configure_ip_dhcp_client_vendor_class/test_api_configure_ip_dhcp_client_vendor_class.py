import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_client_vendor_class


class TestConfigureIpDhcpClientVendorClass(TestCase):

    def test_configure_ip_dhcp_client_vendor_class(self):
        device = Mock()
        result = configure_ip_dhcp_client_vendor_class(device, 'GigabitEthernet0/0/1', 'mac-address', None)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'ip dhcp client vendor-class mac-address'],)
        )

    def test_configure_ip_dhcp_client_vendor_class_1(self):
        device = Mock()
        result = configure_ip_dhcp_client_vendor_class(device, 'GigabitEthernet0/0/1', 'disable', None)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'ip dhcp client vendor-class disable'],)
        )

    def test_configure_ip_dhcp_client_vendor_class_2(self):
        device = Mock()
        result = configure_ip_dhcp_client_vendor_class(device, 'GigabitEthernet0/0/1', 'ascii', 'abcDEF123')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'ip dhcp client vendor-class ascii abcDEF123'],)
        )

    def test_configure_ip_dhcp_client_vendor_class_3(self):
        device = Mock()
        result = configure_ip_dhcp_client_vendor_class(device, 'GigabitEthernet0/0/1', 'hex', '0102030a0b0c')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'ip dhcp client vendor-class hex 0102030a0b0c'],)
        )


if __name__ == '__main__':
    unittest.main()