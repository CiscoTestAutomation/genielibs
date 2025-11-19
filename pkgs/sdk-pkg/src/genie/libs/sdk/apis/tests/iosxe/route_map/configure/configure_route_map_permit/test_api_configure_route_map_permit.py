from unittest import TestCase
from genie.libs.sdk.apis.iosxe.route_map.configure import configure_route_map_permit
from unittest.mock import Mock


class TestConfigureRouteMapPermit(TestCase):

    def test_configure_route_map_permit(self):
        self.device = Mock()
        result = configure_route_map_permit(self.device, 'TEST_RECURSIVE', '40', None, None, None, None, None, None, None, None, None, None, 'Mgmt-vrf', None, 'True', None, '10.106.16.20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['route-map TEST_RECURSIVE permit 40', 'set ip vrf Mgmt-vrf next-hop 10.106.16.20'],)
        )
