import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_dhcp_relay_source_interface_intf_id


class TestConfigureInterfaceIpDhcpRelaySourceInterfaceIntfId(TestCase):

    def test_configure_interface_ip_dhcp_relay_source_interface_intf_id(self):
        device = Mock()
        result = configure_interface_ip_dhcp_relay_source_interface_intf_id(device, 'vlan100', 'Loopback1')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface vlan100', 'ip dhcp relay source-interface Loopback1'],)
        )


if __name__ == '__main__':
    unittest.main()