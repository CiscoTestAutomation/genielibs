from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pbr.configure import configure_pbr_route_map_add_set
from unittest.mock import Mock


class TestConfigurePbrRouteMapAddSet(TestCase):

    def test_configure_pbr_route_map_add_set(self):
        self.device = Mock()
        result = configure_pbr_route_map_add_set(self.device, 'test-rm', '1.2.3.4', '10', '1', '11', 'permit', True, False, None, None, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map test-rm permit 10', 'set ip next-hop verify-availability 1.2.3.4 11 track 1'],)
        )

    def test_configure_pbr_route_map_add_set_1(self):
        self.device = Mock()
        result = configure_pbr_route_map_add_set(self.device, 'test-rm', '1.2.3.4', '10', '', '', 'permit', False, True, None, None, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map test-rm permit 10', 'set ip next-hop recursive 1.2.3.4'],)
        )

    def test_configure_pbr_route_map_add_set_2(self):
        self.device = Mock()
        result = configure_pbr_route_map_add_set(self.device, 'test-rm', '1.2.3.4', '10', '', '', 'permit', False, False, None, None, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map test-rm permit 10', 'set ip next-hop 1.2.3.4'],)
        )
