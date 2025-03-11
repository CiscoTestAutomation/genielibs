from unittest import TestCase
from genie.libs.sdk.apis.iosxe.route_map.configure import unconfigure_route_map
from unittest.mock import Mock


class TestUnconfigureRouteMap(TestCase):

    def test_unconfigure_route_map(self):
        self.device = Mock()
        result = unconfigure_route_map(self.device, 'TEST_GENIE')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no route-map TEST_GENIE'],)
        )
