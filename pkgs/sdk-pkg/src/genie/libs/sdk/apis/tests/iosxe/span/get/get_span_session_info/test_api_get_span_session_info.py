import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError, InvalidCommandError)
from genie.libs.sdk.apis.iosxe.span.get import get_span_session_info


class TestGetSpanSessionInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_span_session_info(self):
        # Schema: ShowMonitorSchema -> {'session': {Any(): {'type': str, ...}}}
        expected_output = {
            'session': {
                '1': {
                    'type': 'Local Session',
                    'status': 'Admin Enabled',
                    'source_ports': {
                        'rx_only': 'Gi0/1/4',
                    },
                    'destination_ports': 'Gi0/1/5',
                    'mtu': 1500,
                }
            }
        }
        self.device.parse.return_value = expected_output
        result = get_span_session_info(self.device, '1')
        self.device.parse.assert_called_once_with('show monitor session 1')
        self.assertEqual(result, expected_output)

    def test_get_span_session_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_span_session_info(self.device, '1')
        self.assertIsNone(result)

    def test_get_span_session_info_invalid_command(self):
        self.device.parse.side_effect = InvalidCommandError("Invalid")
        result = get_span_session_info(self.device, '1')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
