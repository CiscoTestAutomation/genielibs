from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pbr.configure import configure_pbr_route_map


class TestConfigurePbrRouteMap(TestCase):

    def test_configure_pbr_route_map(self):
        device = Mock()
        result = configure_pbr_route_map(
            device,
            'pbrv6_1',
            'aclv6_1',
            '12::1:1',
            None,
            'RED',
            None,
            None,
            '10',
            'permit',
            True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'route-map pbrv6_1 permit 10',
                'match ipv6 address aclv6_1',
                'set ipv6 vrf RED next-hop 12::1:1'
            ],)
        )