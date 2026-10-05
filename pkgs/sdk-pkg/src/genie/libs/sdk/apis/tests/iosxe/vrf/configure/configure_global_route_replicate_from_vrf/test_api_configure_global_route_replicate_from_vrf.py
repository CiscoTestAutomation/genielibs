from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    configure_global_route_replicate_from_vrf,
)


class TestConfigureGlobalRouteReplicateFromVrf(TestCase):

    def test_configure_bgp_route_replicate(self):
        device = Mock()

        configure_global_route_replicate_from_vrf(
            device=device,
            address_family='ipv4',
            source_vrf='tc16_vrf',
            route_protocol='bgp',
            bgp_as=65001,
            route_map='TC16-VRF-TO-GRT')

        device.configure.assert_called_once_with([
            'global-address-family ipv4',
            'route-replicate from vrf tc16_vrf unicast bgp 65001 '
            'route-map TC16-VRF-TO-GRT',
        ])

    def test_configure_connected_route_replicate(self):
        device = Mock()

        configure_global_route_replicate_from_vrf(
            device=device,
            address_family='ipv4',
            source_vrf='tc16_vrf',
            route_protocol='connected')

        device.configure.assert_called_once_with([
            'global-address-family ipv4',
            'route-replicate from vrf tc16_vrf unicast connected',
        ])
