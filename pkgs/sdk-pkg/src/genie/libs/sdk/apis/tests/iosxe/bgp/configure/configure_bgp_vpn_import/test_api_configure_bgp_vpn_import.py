from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_vpn_import

class TestConfigureBgpVpnImport(TestCase):

    def test_configure_bgp_vpn_import(self):
        device = Mock()
        result = configure_bgp_vpn_import(device, 3, 'l2vpn', 'evpn', 'vpnv4', 'unicast', True)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router bgp 3', 'address-family l2vpn evpn', 'import vpnv4 unicast re-originate'],)
        )

    def test_configure_bgp_vpn_import_1(self):
        device = Mock()
        result = configure_bgp_vpn_import(device, 3, 'vpnv4', None, 'l2vpn', 'evpn', False)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router bgp 3', 'address-family vpnv4', 'import l2vpn evpn'],)
        )

    def test_configure_bgp_vpn_import_2(self):
        device = Mock()
        result = configure_bgp_vpn_import(device, 3, 'l2vpn', 'evpn', None, None, True)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router bgp 3', 'address-family l2vpn evpn'],)
        )