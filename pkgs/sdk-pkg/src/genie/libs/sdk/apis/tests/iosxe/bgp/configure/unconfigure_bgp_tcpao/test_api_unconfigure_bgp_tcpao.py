from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_bgp_tcpao
from unittest.mock import Mock


class TestUnconfigureBgpTcpao(TestCase):

    def test_unconfigure_bgp_tcpao(self):
        self.device = Mock()
        result = unconfigure_bgp_tcpao(self.device, 65002, '13.10.0.1', 'test1', 'accept-ao-mismatch-connections', 'ipv4', 'vrf_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 65002', 'address-family ipv4 unicast vrf vrf_1', 'no neighbor 13.10.0.1 ao test1 accept-ao-mismatch-connections'],)
        )
