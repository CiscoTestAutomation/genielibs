from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_route_map


class TestConfigureRouteMap(TestCase):

    def test_configure_route_map(self):
        device = Mock()
        result = configure_route_map(
            device,
            'rm_v4pbr_nexthop1',
            '10',
            None,
            'v4pbr_acl',
            None,
            None,
            None,
            'tunnel20'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('route-map rm_v4pbr_nexthop1 permit 10\nmatch ip address v4pbr_acl\nset interface tunnel20\n',)
        )