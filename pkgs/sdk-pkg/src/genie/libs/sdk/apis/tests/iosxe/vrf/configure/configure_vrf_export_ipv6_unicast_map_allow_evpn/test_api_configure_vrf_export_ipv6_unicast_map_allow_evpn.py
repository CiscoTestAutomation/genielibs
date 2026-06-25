from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vrf_export_ipv6_unicast_map_allow_evpn
from unittest.mock import Mock


class TestConfigureVrfExportIpv6UnicastMapAllowEvpn(TestCase):

    def test_configure_vrf_export_ipv6_unicast_map_allow_evpn(self):
        self.device = Mock()
        result = configure_vrf_export_ipv6_unicast_map_allow_evpn(self.device, 'green', 'RM_EXPORT_IPV6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition green', 'address-family ipv6', 'export ipv6 unicast map RM_EXPORT_IPV6 allow-evpn', 'exit-address-family'],)
        )
