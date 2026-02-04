import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_option43


class TestConfigureDhcpOption43(TestCase):

    def test_configure_dhcp_option43(self):
        device = Mock()
        result = configure_dhcp_option43(device, 'vlan501', 'ascii', '5A1N;B2;K4;I10.197.153.208;J80')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp pool vlan501', 'option 43 ascii 5A1N;B2;K4;I10.197.153.208;J80'],)
        )


if __name__ == '__main__':
    unittest.main()