import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_exclude_vrf


class TestConfigureIpDhcpExcludeVrf(TestCase):

    def test_configure_ip_dhcp_exclude_vrf(self):
        device = Mock()
        result = configure_ip_dhcp_exclude_vrf(device, 'vxlan900001', '172.16.16.1', '172.16.16.9')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp excluded-address vrf vxlan900001 172.16.16.1 172.16.16.9'],)
        )


if __name__ == '__main__':
    unittest.main()