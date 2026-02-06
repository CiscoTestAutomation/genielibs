import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_pool


class TestConfigureDhcpPool(TestCase):

    def test_configure_dhcp_pool(self):
        device = Mock()
        result = configure_dhcp_pool(device, 'POOL_88', None, None, None, None, None, 'True', None, None, None, 'infinite')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp pool POOL_88', 'lease infinite'],)
        )


if __name__ == '__main__':
    unittest.main()