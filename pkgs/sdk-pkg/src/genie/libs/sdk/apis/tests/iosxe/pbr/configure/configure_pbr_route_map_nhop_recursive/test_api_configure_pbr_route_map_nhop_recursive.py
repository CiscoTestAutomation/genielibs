from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pbr.configure import configure_pbr_route_map_nhop_recursive
from unittest.mock import Mock


class TestConfigurePbrRouteMapNhopRecursive(TestCase):

    def test_configure_pbr_route_map_nhop_recursive(self):
        self.device = Mock()
        result = configure_pbr_route_map_nhop_recursive(self.device, 'pbr-route-map', '1.2.3.4', 'pbr-acl', None, '10', 'permit', False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map pbr-route-map permit 10', 'match ip address pbr-acl', 'set ip next-hop recursive 1.2.3.4'],)
        )
