from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_pool
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpPool(TestCase):

    def test_unconfigure_ipv6_dhcp_pool(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_pool(self.device, 'POOL_88')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 dhcp pool POOL_88'],)
        )
