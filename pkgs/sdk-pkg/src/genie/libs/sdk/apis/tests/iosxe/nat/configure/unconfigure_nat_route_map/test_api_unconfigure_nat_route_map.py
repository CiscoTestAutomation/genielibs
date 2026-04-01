from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_route_map

class TestUnconfigureNatRouteMap(TestCase):

    def test_unconfigure_nat_route_map(self):
        device = Mock()
        result = unconfigure_nat_route_map(device, 'acl_test', 'permit', 10)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no route-map acl_test permit 10',)
        )