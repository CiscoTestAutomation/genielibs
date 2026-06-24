import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.span.get import (
    get_span_session_running_config)


class TestGetSpanSessionRunningConfig(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_source_with_direction_and_destination(self):
        self.device.api.get_running_config_section.return_value = [
            'monitor session 1 source interface Gi0/1/4 rx',
            'monitor session 1 destination interface Gi0/1/5',
        ]
        result = get_span_session_running_config(self.device)
        self.assertEqual(result, [
            {
                'id': '1',
                'role': 'source',
                'intf': 'Gi0/1/4',
                'direction': 'rx',
            },
            {
                'id': '1',
                'role': 'destination',
                'intf': 'Gi0/1/5',
                'direction': None,
            },
        ])

    def test_source_default_direction_both(self):
        self.device.api.get_running_config_section.return_value = [
            'monitor session 2 source interface Gi0/1/6',
        ]
        result = get_span_session_running_config(self.device)
        self.assertEqual(result, [
            {
                'id': '2',
                'role': 'source',
                'intf': 'Gi0/1/6',
                'direction': 'both',
            },
        ])

    def test_no_matching_lines(self):
        self.device.api.get_running_config_section.return_value = [
            'no monitor session 1',
            'some other config',
        ]
        result = get_span_session_running_config(self.device)
        self.assertEqual(result, [])

    def test_empty_input(self):
        self.device.api.get_running_config_section.return_value = []
        result = get_span_session_running_config(self.device)
        self.assertEqual(result, [])

    def test_none_input(self):
        self.device.api.get_running_config_section.return_value = None
        result = get_span_session_running_config(self.device)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
