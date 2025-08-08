from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_ospf_internal_external_routes_into_bgp
from unittest.mock import Mock

class TestConfigureOspfInternalExternalRoutesIntoBgp(TestCase):

    def test_configure_ospf_internal_external_routes_into_bgp(self):
        self.device = Mock()
        configure_ospf_internal_external_routes_into_bgp(self.device, 3, 3, 'green', 'ipv4', 10)
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 3', 'address-family ipv4 vrf green', 'redistribute ospf 3 match internal external 1 external 2 metric 10'],))  
        
    def test_configure_ospf_internal_external_routes_into_bgp_1(self):
        self.device = Mock()
        configure_ospf_internal_external_routes_into_bgp(self.device, 3, 3, None, 'ipv4', 10)
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 3',  'redistribute ospf 3 match internal external 1 external 2 metric 10'],))
        
    def test_configure_ospf_internal_external_routes_into_bgp_2(self):
        self.device = Mock()
        configure_ospf_internal_external_routes_into_bgp(self.device, 3, 3, 'green', 'ipv4', None)
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 3','address-family ipv4 vrf green', 'redistribute ospf 3 match internal external 1 external 2'],))
        

    def test_configure_ospf_internal_external_routes_into_bgp_3(self):
        self.device = Mock()
        configure_ospf_internal_external_routes_into_bgp(self.device, 3, 3, None, 'ipv4', None)
        self.assertEqual(self.device.configure.mock_calls[0].args, ((['router bgp 3', 'redistribute ospf 3 match internal external 1 external 2'],)))