from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_route_map

class TestConfigureNatRouteMap(TestCase):

    def test_configure_nat_route_map(self):
        device = Mock()
        result = configure_nat_route_map(device, 'acl_test', 'permit', 10, 'acl_t')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'route-map acl_test permit 10',
                'match ip address acl_t'
            ],)
        )