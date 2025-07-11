from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_advertise_l2vpn_evpn
from unittest.mock import Mock

class TestConfigureBgpAdvertiseL2vpnEvpn(TestCase):

    def test_configure_bgp_advertise_l2vpn_evpn(self):
        self.device = Mock()
        configure_bgp_advertise_l2vpn_evpn(self.device, 1, 'ipv6', 'green')
        self.device.configure.assert_called_with(['router bgp 1', 'address-family ipv6 vrf green', 'advertise l2vpn evpn'])
