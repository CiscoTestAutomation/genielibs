import unittest
from unittest.mock import Mock, call, patch

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_ap_fabric_summary,
)


class OneAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations == 1

    def sleep(self):
        return None


class TestVerifyApFabricSummary(unittest.TestCase):

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_ap_fabric_summary(self):
        device = Mock()
        device.api.get_fabric_ap_state.side_effect = [
            'Registered',
            'registered',
        ]

        result = verify_ap_fabric_summary(device, ['AP1', 'AP2'])

        self.assertTrue(result)
        device.api.get_fabric_ap_state.assert_has_calls([
            call('AP1'),
            call('AP2'),
        ])

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_ap_fabric_summary_not_registered(self):
        device = Mock()
        device.api.get_fabric_ap_state.return_value = 'Not Registered'

        result = verify_ap_fabric_summary(device, ['AP1'])

        self.assertFalse(result)
