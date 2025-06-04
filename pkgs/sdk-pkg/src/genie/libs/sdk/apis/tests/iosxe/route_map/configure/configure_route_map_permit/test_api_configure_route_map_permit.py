from unittest import TestCase
from genie.libs.sdk.apis.iosxe.route_map.configure import configure_route_map_permit
from unittest.mock import Mock


class TestConfigureRouteMapPermit(TestCase):

    def test_configure_route_map_permit(self):
        self.device = Mock()
        result = configure_route_map_permit(self.device, 'TEST_GENIE', '40', None, None, None, None, None, None, None, None, None, None, 'TEST2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map TEST_GENIE permit 40', 'set vrf TEST2'],)
        )
