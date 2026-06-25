from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vrf_export_ipv4_unicast_map_allow_evpn
from unittest.mock import Mock


class TestConfigureVrfExportIpv4UnicastMapAllowEvpn(TestCase):

    def test_configure_vrf_export_ipv4_unicast_map_allow_evpn(self):
        self.device = Mock()
        result = configure_vrf_export_ipv4_unicast_map_allow_evpn(self.device, 'green', 'RM_EXPORT_IPV4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition green', 'address-family ipv4', 'export ipv4 unicast map RM_EXPORT_IPV4 allow-evpn', 'exit-address-family'],)
        )
