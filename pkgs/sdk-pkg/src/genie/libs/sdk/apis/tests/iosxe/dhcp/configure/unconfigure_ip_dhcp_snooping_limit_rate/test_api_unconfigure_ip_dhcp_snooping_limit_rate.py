from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_limit_rate
from unittest.mock import Mock


class TestUnconfigureIpDhcpSnoopingLimitRate(TestCase):

    def test_unconfigure_ip_dhcp_snooping_limit_rate(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_limit_rate(self.device, 'GigabitEthernet1/0/5', '15')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/5', 'no ip dhcp snooping limit rate 15'],)
        )
