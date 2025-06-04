from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_restrict_next_hop
from unittest.mock import Mock


class TestUnconfigureIpDhcpRestrictNextHop(TestCase):

    def test_unconfigure_ip_dhcp_restrict_next_hop(self):
        self.device = Mock()
        unconfigure_ip_dhcp_restrict_next_hop(self.device, 'GigabitEthernet1/0/1')
        self.assertEqual(
        self.device.configure.mock_calls[0].args,
        (['interface GigabitEthernet1/0/1', 'no ip dhcp restrict-next-hop'],)
    )