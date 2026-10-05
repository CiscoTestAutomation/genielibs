import unittest
from unittest.mock import Mock, patch

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_ap_mode,
)


class TwoAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations <= 2

    def sleep(self):
        return None


class TestVerifyApMode(unittest.TestCase):

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        TwoAttemptTimeout,
    )
    def test_verify_ap_mode_retries_until_registered(self):
        device = Mock()
        device.api.get_ap_mode.side_effect = ['', 'LOCAL']

        result = verify_ap_mode(device, ['AP1'])

        self.assertTrue(result)
        self.assertEqual(device.api.get_ap_mode.call_count, 2)

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        TwoAttemptTimeout,
    )
    def test_verify_ap_mode_mismatch(self):
        device = Mock()
        device.api.get_ap_mode.return_value = 'flex'

        result = verify_ap_mode(device, ['AP1'], ap_mode='local')

        self.assertFalse(result)
        device.api.get_ap_mode.assert_called_once_with('AP1')
