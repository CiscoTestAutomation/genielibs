import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.route_map.configure import (
    configure_route_map_route_map
)


class TestConfigureRouteMapRouteMap(unittest.TestCase):

    def test_configure_route_map_route_map(self):
        device = Mock()

        result = configure_route_map_route_map(
            device,
            [{
                'continue_id': '20',
                'local_preference': '500',
                'match_as_path': '12',
                'route_map': 'internal',
                'seq': '10',
                'set_as_path_prepend': '45000',
                'set_metric': '30',
                'set_weight': '100'
            }]
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('route-map internal permit 10\n',) 
            )