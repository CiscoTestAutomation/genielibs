import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    configure_ipv6_route_nexthop_vrf
)


class TestConfigureIpv6RouteNexthopVrf(unittest.TestCase):

    def test_configure_ipv6_route_nexthop_vrf(self):
        device = Mock()

        result = configure_ipv6_route_nexthop_vrf(
            device,
            '2009::/64',
            'TenGigabitEthernet2/2/0/35',
            'vrf1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ipv6 route 2009::/64 TenGigabitEthernet2/2/0/35 nexthop-vrf vrf1',)
        )