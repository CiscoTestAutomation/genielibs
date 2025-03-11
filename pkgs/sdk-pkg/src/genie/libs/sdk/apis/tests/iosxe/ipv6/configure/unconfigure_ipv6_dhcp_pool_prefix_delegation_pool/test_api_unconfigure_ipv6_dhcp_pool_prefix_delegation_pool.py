from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import unconfigure_ipv6_dhcp_pool_prefix_delegation_pool
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpPoolPrefixDelegationPool(TestCase):

    def test_unconfigure_ipv6_dhcp_pool_prefix_delegation_pool(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_pool_prefix_delegation_pool(self.device, 'ipv6_dhcp_pool', 'ipv6_local_pool')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp pool ipv6_dhcp_pool', 'no prefix-delegation pool ipv6_local_pool'],)
        )
