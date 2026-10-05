from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.bgp.configure import (
    unconfigure_bgp_advertise_l2vpn_evpn,
)


class TestUnconfigureBgpAdvertiseL2vpnEvpn(TestCase):

    def test_unconfigure_bgp_advertise_l2vpn_evpn(self):
        device = Mock()

        unconfigure_bgp_advertise_l2vpn_evpn(
            device=device,
            bgp_as=65001,
            address_family='ipv4',
            vrf='green')

        device.configure.assert_called_once_with([
            'router bgp 65001',
            'address-family ipv4 vrf green',
            'no advertise l2vpn evpn',
        ])
