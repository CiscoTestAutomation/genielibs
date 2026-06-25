from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import unconfigure_vrf_ipv4_unicast_map_allow_evpn
from unittest.mock import Mock


class TestUnconfigureVrfIpv4UnicastMapAllowEvpn(TestCase):

    def test_unconfigure_vrf_ipv4_unicast_map_allow_evpn(self):
        self.device = Mock()
        result = unconfigure_vrf_ipv4_unicast_map_allow_evpn(self.device, 'green', 'RM_EXPORT_IPV4', 'RM_IMPORT_IPV4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition green', 'address-family ipv4', 'no export ipv4 unicast map RM_EXPORT_IPV4 allow-evpn', 'no import ipv4 unicast map RM_IMPORT_IPV4 allow-evpn', 'exit-address-family'],)
        )
