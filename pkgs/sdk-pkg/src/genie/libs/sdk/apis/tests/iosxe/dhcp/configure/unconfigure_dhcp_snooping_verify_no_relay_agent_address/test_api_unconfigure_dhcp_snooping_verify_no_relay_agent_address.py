import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_snooping_verify_no_relay_agent_address


class TestUnconfigureDhcpSnoopingVerifyNoRelayAgentAddress(TestCase):

    def test_unconfigure_dhcp_snooping_verify_no_relay_agent_address(self):
        device = Mock()
        result = unconfigure_dhcp_snooping_verify_no_relay_agent_address(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('no ip dhcp snooping verify no-relay-agent-address')


if __name__ == '__main__':
    unittest.main()