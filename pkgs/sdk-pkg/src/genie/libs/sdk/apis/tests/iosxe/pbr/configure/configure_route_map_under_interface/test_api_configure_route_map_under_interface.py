from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.pbr.configure import configure_route_map_under_interface


class TestConfigureRouteMapUnderInterface(TestCase):

    def test_configure_route_map_under_interface(self):
        device = Mock()
        result = configure_route_map_under_interface(
            device,
            'Fi1/0/5',
            'rm_v4pbr_nexthop1',
            False
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Fi1/0/5', 'ip policy route-map rm_v4pbr_nexthop1'],)
        )