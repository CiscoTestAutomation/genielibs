import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.l2qos.get import (
    get_show_wrr_queue_bandwidth)


class TestGetShowWrrQueueBandwidth(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_bandwidth(self):
        expected_output = {
            'enabled': True,
            'interface_type': 'Etherswitch NGWIC',
            'queues': {
                1: {'bandwidth': 1},
                2: {'bandwidth': 2},
                3: {'bandwidth': 3},
                4: {'bandwidth': 6},
            },
        }
        self.device.parse.return_value = expected_output
        result = get_show_wrr_queue_bandwidth(self.device)
        self.device.parse.assert_called_once_with(
            'show wrr-queue bandwidth')
        self.assertEqual(result, expected_output)

    def test_get_bandwidth_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_show_wrr_queue_bandwidth(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
