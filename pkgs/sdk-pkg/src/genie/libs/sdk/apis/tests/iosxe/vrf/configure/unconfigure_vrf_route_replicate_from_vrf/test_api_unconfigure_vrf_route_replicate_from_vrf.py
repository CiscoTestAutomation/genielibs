from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vrf.configure import (
    unconfigure_vrf_route_replicate_from_vrf,
)


class TestUnconfigureVrfRouteReplicateFromVrf(TestCase):

    def test_unconfigure_bgp_route_replicate(self):
        device = Mock()

        unconfigure_vrf_route_replicate_from_vrf(
            device=device,
            vrf_name='tc13_external',
            address_family='ipv4',
            source_vrf='green',
            route_protocol='bgp',
            bgp_as=65001,
            route_map='TC13-GREEN-TO-EXTERNAL')

        device.configure.assert_called_once_with([
            'vrf definition tc13_external',
            'address-family ipv4',
            'no route-replicate from vrf green unicast bgp 65001 '
            'route-map TC13-GREEN-TO-EXTERNAL',
            'exit-address-family',
        ])

    def test_unconfigure_connected_route_replicate(self):
        device = Mock()

        unconfigure_vrf_route_replicate_from_vrf(
            device=device,
            vrf_name='green',
            address_family='ipv4',
            source_vrf='tc13_external',
            route_protocol='connected')

        device.configure.assert_called_once_with([
            'vrf definition green',
            'address-family ipv4',
            'no route-replicate from vrf tc13_external unicast connected',
            'exit-address-family',
        ])
