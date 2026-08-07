import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.l2qos.get import (
    get_show_wrr_queue_cos_map)


class TestGetShowWrrQueueCosMap(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_cos_map(self):
        expected_output = {
            'interface_type': 'Etherswitch NGWIC',
            'cos_map': {
                0: {'priority_queue': 1},
                1: {'priority_queue': 5},
                2: {'priority_queue': 3},
                3: {'priority_queue': 4},
                4: {'priority_queue': 5},
                5: {'priority_queue': 6},
                6: {'priority_queue': 7},
                7: {'priority_queue': 8},
            },
        }
        self.device.parse.return_value = expected_output
        result = get_show_wrr_queue_cos_map(self.device)
        self.device.parse.assert_called_once_with(
            'show wrr-queue cos-map')
        self.assertEqual(result, expected_output)

    def test_get_cos_map_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_show_wrr_queue_cos_map(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
