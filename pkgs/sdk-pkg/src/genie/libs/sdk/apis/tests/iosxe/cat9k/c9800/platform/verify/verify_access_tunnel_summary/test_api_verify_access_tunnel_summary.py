import unittest
from unittest.mock import Mock, patch

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_access_tunnel_summary,
)


class OneAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations == 1

    def sleep(self):
        return None


class TwoAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations <= 2

    def sleep(self):
        return None


class TestVerifyAccessTunnelSummary(unittest.TestCase):

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        TwoAttemptTimeout,
    )
    def test_verify_access_tunnel_summary_retries(self):
        device = Mock()
        device.api.get_ap_ip.side_effect = ['70.201.2.151', '70.201.2.152']
        device.api.get_rloc_ip.return_value = '70.1.1.1'

        result = verify_access_tunnel_summary(
            device,
            ap_name='AP1',
            ap_ip='70.201.2.152',
            rloc_ip='70.1.1.1',
        )

        self.assertTrue(result)
        self.assertEqual(device.api.get_ap_ip.call_count, 2)
        self.assertEqual(device.api.get_rloc_ip.call_count, 2)

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_access_tunnel_summary_mismatch(self):
        device = Mock()
        device.api.get_ap_ip.return_value = '70.201.2.151'
        device.api.get_rloc_ip.return_value = '70.1.1.2'

        result = verify_access_tunnel_summary(
            device,
            ap_name='AP1',
            ap_ip='70.201.2.152',
            rloc_ip='70.1.1.1',
        )

        self.assertFalse(result)
