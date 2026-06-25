from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import unconfigure_vrf_ipv6_unicast_map_allow_evpn
from unittest.mock import Mock


class TestUnconfigureVrfIpv6UnicastMapAllowEvpn(TestCase):

    def test_unconfigure_vrf_ipv6_unicast_map_allow_evpn(self):
        self.device = Mock()
        result = unconfigure_vrf_ipv6_unicast_map_allow_evpn(self.device, 'green', 'RM_EXPORT_IPV6', 'RM_IMPORT_IPV6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition green', 'address-family ipv6', 'no export ipv6 unicast map RM_EXPORT_IPV6 allow-evpn', 'no import ipv6 unicast map RM_IMPORT_IPV6 allow-evpn', 'exit-address-family'],)
        )
