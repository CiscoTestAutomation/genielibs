from unittest import TestCase
from genie.libs.sdk.apis.iosxe.route_map.configure import unconfigure_route_map_permit
from unittest.mock import Mock


class TestUnconfigureRouteMapPermit(TestCase):

    def test_unconfigure_route_map_permit(self):
        self.device = Mock()
        result = unconfigure_route_map_permit(self.device, 'TEST_GENIE', '10', None, None, None, None, None, None, None, None, None, 'RECURSIVE1', None, '1', '10.106.16.20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map TEST_GENIE permit 10', 'no set ip default next-hop recursive vrf RECURSIVE1 10.106.16.20'],)
        )
