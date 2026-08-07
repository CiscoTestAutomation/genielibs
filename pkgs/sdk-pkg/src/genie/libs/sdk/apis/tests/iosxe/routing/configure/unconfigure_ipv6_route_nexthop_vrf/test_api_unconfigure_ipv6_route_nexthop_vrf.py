import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    unconfigure_ipv6_route_nexthop_vrf
)


class TestUnconfigureIpv6RouteNexthopVrf(unittest.TestCase):

    def test_unconfigure_ipv6_route_nexthop_vrf(self):
        device = Mock()

        result = unconfigure_ipv6_route_nexthop_vrf(
            device,
            '2009::/64',
            'TenGigabitEthernet2/2/0/35',
            'vrf1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 route 2009::/64 TenGigabitEthernet2/2/0/35 nexthop-vrf vrf1',)
        )