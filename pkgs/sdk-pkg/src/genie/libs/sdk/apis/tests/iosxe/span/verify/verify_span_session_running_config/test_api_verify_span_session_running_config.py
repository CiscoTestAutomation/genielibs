import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.span.verify import (
    verify_span_session_running_config)


def _build_device():
    device = Mock()
    return device


class TestVerifySpanSessionRunningConfig(unittest.TestCase):

    def test_match_source_with_direction(self):
        device = _build_device()
        device.api.get_span_session_running_config.return_value = [
            {'id': '1', 'role': 'source',
             'intf': 'Gi0/1/4', 'direction': 'rx'},
            {'id': '1', 'role': 'destination',
             'intf': 'Gi0/1/5', 'direction': None},
        ]
        self.assertTrue(verify_span_session_running_config(
            device, '1', 'source', 'GigabitEthernet0/1/4',
            direction='rx'))

    def test_match_destination_no_direction(self):
        device = _build_device()
        device.api.get_span_session_running_config.return_value = [
            {'id': '1', 'role': 'destination',
             'intf': 'Gi0/1/5', 'direction': None},
        ]
        self.assertTrue(verify_span_session_running_config(
            device, '1', 'destination', 'GigabitEthernet0/1/5'))

    def test_match_short_interface_argument(self):
        device = _build_device()
        device.api.get_span_session_running_config.return_value = [
            {'id': '1', 'role': 'source',
             'intf': 'Gi0/1/4', 'direction': 'rx'},
        ]
        # Interface passed in short form must still match the short form
        # stored in the running config.
        self.assertTrue(verify_span_session_running_config(
            device, '1', 'source', 'Gi0/1/4', direction='rx'))

    def test_unmodeled_interface_does_not_raise(self):
        device = _build_device()
        # device.interfaces lookup must never be used; accessing it raises
        # KeyError to prove the API works from the interface string alone.
        device.interfaces = {}
        device.api.get_span_session_running_config.return_value = [
            {'id': '1', 'role': 'source',
             'intf': 'Gi0/1/4', 'direction': 'rx'},
        ]
        self.assertTrue(verify_span_session_running_config(
            device, '1', 'source', 'GigabitEthernet0/1/4',
            direction='rx'))

    def test_no_match_returns_false(self):
        device = _build_device()
        device.api.get_span_session_running_config.return_value = [
            {'id': '2', 'role': 'source',
             'intf': 'Gi0/1/4', 'direction': 'rx'},
        ]
        self.assertFalse(verify_span_session_running_config(
            device, '1', 'source', 'GigabitEthernet0/1/4',
            direction='rx'))

    def test_empty_config_returns_false(self):
        device = _build_device()
        device.api.get_span_session_running_config.return_value = []
        self.assertFalse(verify_span_session_running_config(
            device, '1', 'source', 'GigabitEthernet0/1/4',
            direction='rx'))

    def test_expect_not_exist_when_missing(self):
        device = _build_device()
        device.api.get_span_session_running_config.return_value = [
            {'id': '2', 'role': 'source',
             'intf': 'Gi0/1/4', 'direction': 'rx'},
        ]
        self.assertTrue(verify_span_session_running_config(
            device, '1', 'source', 'GigabitEthernet0/1/4',
            direction='rx', expect_exist=False))

    def test_expect_not_exist_when_present_fails(self):
        device = _build_device()
        device.api.get_span_session_running_config.return_value = [
            {'id': '1', 'role': 'source',
             'intf': 'Gi0/1/4', 'direction': 'rx'},
        ]
        self.assertFalse(verify_span_session_running_config(
            device, '1', 'source', 'GigabitEthernet0/1/4',
            direction='rx', expect_exist=False))


if __name__ == '__main__':
    unittest.main()
