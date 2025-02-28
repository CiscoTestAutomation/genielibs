from unittest import TestCase
from genie.libs.sdk.apis.iosxe.route_map.configure import configure_route_map_with_description
from unittest.mock import Mock


class TestConfigureRouteMapWithDescription(TestCase):

    def test_configure_route_map_with_description(self):
        self.device = Mock()
        result = configure_route_map_with_description(self.device, 'TEST_GENIE', '34', 'THIS IS GENIE')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map TEST_GENIE permit 34', 'description THIS IS GENIE'],)
        )
