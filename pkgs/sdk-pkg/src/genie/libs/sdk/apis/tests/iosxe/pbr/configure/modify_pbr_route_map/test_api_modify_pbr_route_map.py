from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pbr.configure import modify_pbr_route_map


class TestModifyPbrRouteMap(TestCase):

    def test_modify_pbr_route_map(self):
        device = Mock()
        result = modify_pbr_route_map(
            device,
            'pbrsvi6',
            'asvi1',
            '12::1:1',
            True,
            'RED',
            None,
            None,
            '10',
            'permit',
            True,
            False,
            True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'route-map pbrsvi6 permit 10',
                'no set ipv6 default vrf RED next-hop 12::1:1'
            ],)
        )