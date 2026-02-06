import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import create_dhcp_pool_withoutrouter


class TestCreateDhcpPoolWithoutrouter(TestCase):

    def test_create_dhcp_pool_withoutrouter(self):
        device = Mock()
        result = create_dhcp_pool_withoutrouter(device, 'VLAN_10', '10.10.10.0', '255.255.255.0', '0', '0', '35')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp pool VLAN_10', 'network  10.10.10.0 255.255.255.0', 'lease 0 0 35'],)
        )


if __name__ == '__main__':
    unittest.main()