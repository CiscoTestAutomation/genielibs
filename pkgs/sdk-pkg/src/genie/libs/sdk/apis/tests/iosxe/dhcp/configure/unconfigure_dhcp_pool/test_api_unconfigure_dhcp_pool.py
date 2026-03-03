import unittest
from unittest import TestCase
from unittest.mock import Mock, ANY
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_pool


class TestUnconfigureDhcpPool(TestCase):

    def test_unconfigure_dhcp_pool(self):
        device = Mock()
        result = unconfigure_dhcp_pool(device, 'vlan501', None, '1.1.1.0', '255.255.255.0', 'Mgmt-vrf', None)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with(
            [
                'ip dhcp pool vlan501',
                'no network 1.1.1.0 255.255.255.0',
                'no vrf Mgmt-vrf'
            ],
            reply=ANY
        )


if __name__ == '__main__':
    unittest.main()