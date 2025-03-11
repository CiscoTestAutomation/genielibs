from unittest import TestCase
from genie.libs.sdk.apis.iosxe.route_map.configure import route_map_unconfigure_description
from unittest.mock import Mock


class TestRouteMapUnconfigureDescription(TestCase):

    def test_route_map_unconfigure_description(self):
        self.device = Mock()
        result = route_map_unconfigure_description(self.device, 'TEST_GENIE', '34', 'THIS IS GENIE')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map TEST_GENIE permit 34', 'no description THIS IS GENIE'],)
        )
