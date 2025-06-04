from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_trust
from unittest.mock import Mock 

class TestUnconfigureIpDhcpSnoopingTrust(TestCase):

    def test_unconfigure_ip_dhcp_snooping_trust(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_trust(self.device, 'g1/1/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface g1/1/1', 'no ip dhcp snooping trust'],)
        )
