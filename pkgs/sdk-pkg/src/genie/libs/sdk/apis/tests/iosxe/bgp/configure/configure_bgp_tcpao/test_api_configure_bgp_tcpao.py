from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_tcpao
from unittest.mock import Mock


class TestConfigureBgpTcpao(TestCase):

    def test_configure_bgp_tcpao(self):
        self.device = Mock()
        result = configure_bgp_tcpao(self.device, 65002, '13.10.0.1', 'test1', 'include-tcp-options', 'ipv4', 'vrf_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 65002', 'address-family ipv4 unicast vrf vrf_1', 'neighbor 13.10.0.1 ao test1 include-tcp-options'],)
        )
