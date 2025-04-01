from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pbr.configure import configure_pbr_route_map_nhop_verify_availability
from unittest.mock import Mock


class TestConfigurePbrRouteMapNhopVerifyAvailability(TestCase):

    def test_configure_pbr_route_map_nhop_verify_availability(self):
        self.device = Mock()
        result = configure_pbr_route_map_nhop_verify_availability(self.device, 'pbr-route-map', 1, '1.2.3.4', '10', 'pbr-acl', None, None, '10', 'permit', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map pbr-route-map permit 10', 'match ip  address pbr-acl', 'set ip next-hop verify-availability 1.2.3.4 10 track 1'],)
        )
