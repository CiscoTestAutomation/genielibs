import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_snooping_verify_no_relay_agent_address


class TestConfigureDhcpSnoopingVerifyNoRelayAgentAddress(TestCase):

    def test_configure_dhcp_snooping_verify_no_relay_agent_address(self):
        device = Mock()
        result = configure_dhcp_snooping_verify_no_relay_agent_address(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip dhcp snooping verify no-relay-agent-address',)
        )


if __name__ == '__main__':
    unittest.main()