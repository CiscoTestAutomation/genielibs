import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.route_map.configure import (
    unconfigure_route_map_permit
)


class TestUnconfigureRouteMapPermit(unittest.TestCase):

    def test_unconfigure_route_map_permit(self):
        device = Mock()

        result = unconfigure_route_map_permit(
            device,
            'TEST_RECURSIVE',
            '40',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            'Mgmt-vrf',
            None,
            'True',
            None,
            '10.106.16.20'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['route-map TEST_RECURSIVE permit 40',
              'no set ip vrf Mgmt-vrf next-hop 10.106.16.20'],)
        )