from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_ospf_redistribute_in_bgp
from unittest.mock import Mock

class TestConfigureOspfRedistributeInBgp(TestCase):

    def test_configure_ospf_redistribute_in_bgp(self):
        self.device = Mock()
        configure_ospf_redistribute_in_bgp(self.device, 3, 'ipv6', 10, 'internal external 1 external 2', 6, 'test')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 3', 'address-family ipv6', 'redistribute ospf 10 match internal external 1 external 2 metric 6 ''route-map test','exit-address-family'],))

    def test_configure_ospf_redistribute_in_bgp_1(self):
        self.device = Mock()
        configure_ospf_redistribute_in_bgp(self.device, 3, 'ipv6', 10, None, 6, 'test')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 3', 'address-family ipv6', 'redistribute ospf 10 metric 6 route-map test','exit-address-family'],))

    def test_configure_ospf_redistribute_in_bgp_2(self):
        self.device = Mock()
        configure_ospf_redistribute_in_bgp(self.device, 3, 'ipv6', 10, None, None, 'test')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 3', 'address-family ipv6', 'redistribute ospf 10 route-map test','exit-address-family'],))