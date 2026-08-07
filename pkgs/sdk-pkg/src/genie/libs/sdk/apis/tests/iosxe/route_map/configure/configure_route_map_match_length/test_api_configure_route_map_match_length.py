import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.route_map.configure import (
    configure_route_map_match_length
)


class TestConfigureRouteMapMatchLength(unittest.TestCase):

    def test_configure_route_map_match_length(self):
        device = Mock()

        result = configure_route_map_match_length(
            device,
            'green',
            332,
            4533
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
           (['route-map green', 'match length 332 4533'],)
        )