from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_verify
from unittest.mock import Mock

class TestUnconfigureIpDhcpSnoopingVerify(TestCase):

    def test_unconfigure_ip_dhcp_snooping_verify(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_verify(self.device, 'no-relay-agent-address')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dhcp snooping verify no-relay-agent-address',)
        )
