from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_ipv6_neighbor_list
from unittest.mock import Mock


class TestConfigureBgpIpv6NeighborList(TestCase):

    def test_configure_bgp_ipv6_neighbor_list(self):
        self.device = Mock()
        result = configure_bgp_ipv6_neighbor_list(self.device, 50, '20::2', 'prefix-list', '1', 'in')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 50', 'address-family ipv6', 'neighbor 20::2 prefix-list 1 in', 'exit-address-family'],)
        )
