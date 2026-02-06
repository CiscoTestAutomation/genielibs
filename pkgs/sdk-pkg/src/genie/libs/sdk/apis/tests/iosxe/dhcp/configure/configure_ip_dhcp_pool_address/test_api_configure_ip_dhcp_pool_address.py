import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_pool_address


class TestConfigureIpDhcpPoolAddress(TestCase):

    def test_configure_ip_dhcp_pool_address(self):
        device = Mock()
        result = configure_ip_dhcp_pool_address(device, 'vlan501', '1.1.1.1', '0063.6973.636f.2d30.3062.362e.3730.3337.2e39.6630.302d.4769.302f.30')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp pool vlan501', 'address 1.1.1.1 client-id 0063.6973.636f.2d30.3062.362e.3730.3337.2e39.6630.302d.4769.302f.30'],)
        )


if __name__ == '__main__':
    unittest.main()