import unittest
from unittest.mock import Mock, call, patch

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_wireless_process,
)


class OneAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations == 1

    def sleep(self):
        return None


class TestVerifyWirelessProcess(unittest.TestCase):

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_wireless_process(self):
        device = Mock()
        device.api.get_matching_line_processes_platform.return_value = 1
        device.api.get_processes_platform_dict.return_value = {'state': 'up'}
        device.api.get_matching_line_platform_software.return_value = 1
        device.api.get_platform_software_dict.return_value = {'state': 'up'}

        result = verify_wireless_process(device, ['wncd', 'wncmgrd'])

        self.assertTrue(result)
        device.api.get_matching_line_processes_platform.assert_has_calls([
            call('wncd'),
            call('wncmgrd'),
        ])
        device.api.get_processes_platform_dict.assert_has_calls([
            call('wncd'),
            call('wncmgrd'),
        ])
        device.api.get_matching_line_platform_software.assert_has_calls([
            call('wncd'),
            call('wncmgrd'),
        ])
        device.api.get_platform_software_dict.assert_has_calls([
            call('wncd'),
            call('wncmgrd'),
        ])

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_wireless_process_not_running(self):
        device = Mock()
        device.api.get_matching_line_processes_platform.return_value = ''

        result = verify_wireless_process(device, ['wncd'])

        self.assertFalse(result)
        device.api.get_processes_platform_dict.assert_not_called()
