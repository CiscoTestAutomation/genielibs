import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.routing.configure import (
    remove_static_route_all
)


class TestRemoveStaticRouteAll(unittest.TestCase):

    def test_remove_static_route_all(self):
        device = Mock()

        result = remove_static_route_all(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip route *',)
        )