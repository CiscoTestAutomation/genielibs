from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_vrf_import_ipv6_unicast_map_allow_evpn
from unittest.mock import Mock


class TestConfigureVrfImportIpv6UnicastMapAllowEvpn(TestCase):

    def test_configure_vrf_import_ipv6_unicast_map_allow_evpn(self):
        self.device = Mock()
        result = configure_vrf_import_ipv6_unicast_map_allow_evpn(self.device, 'green', 'RM_IMPORT_IPV6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition green', 'address-family ipv6', 'import ipv6 unicast map RM_IMPORT_IPV6 allow-evpn', 'exit-address-family'],)
        )
