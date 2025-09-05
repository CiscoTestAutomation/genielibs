from unittest import TestCase
from genie.libs.sdk.apis.iosxe.route_map.configure import configure_route_map_permit
from unittest.mock import Mock


class TestConfigureRouteMapPermit(TestCase):

    def test_configure_route_map_permit(self):
        self.device = Mock()
        result = configure_route_map_permit(self.device, 'TEST_GENIE', '10', None, None, None, None, None, None, None, None, None, None, 'RECURSIVE1', None, '1', '10.106.16.20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map TEST_GENIE permit 10', 'set vrf RECURSIVE1', 'set ip default next-hop recursive vrf RECURSIVE1 10.106.16.20'],)
        )
