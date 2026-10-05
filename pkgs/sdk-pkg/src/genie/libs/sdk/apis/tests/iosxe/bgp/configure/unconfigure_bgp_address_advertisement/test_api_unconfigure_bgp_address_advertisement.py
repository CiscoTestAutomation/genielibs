from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.bgp.configure import (
    unconfigure_bgp_address_advertisement,
)


class TestUnconfigureBgpAddressAdvertisement(TestCase):

    def test_unconfigure_ipv4_vrf_network(self):
        device = Mock()

        unconfigure_bgp_address_advertisement(
            device=device,
            bgp_as=65001,
            address_family='ipv4',
            ip_address='0.0.0.0',
            mask='0.0.0.0',
            vrf='green')

        device.configure.assert_called_once_with([
            'router bgp 65001',
            'address-family ipv4 vrf green',
            'no network 0.0.0.0 mask 0.0.0.0',
        ])

    def test_unconfigure_ipv6_vrf_network(self):
        device = Mock()

        unconfigure_bgp_address_advertisement(
            device=device,
            bgp_as=65001,
            address_family='ipv6',
            ip_address='2001:db8:1::',
            mask='64',
            vrf='green')

        device.configure.assert_called_once_with([
            'router bgp 65001',
            'address-family ipv6 vrf green',
            'no network 2001:db8:1::/64',
        ])
