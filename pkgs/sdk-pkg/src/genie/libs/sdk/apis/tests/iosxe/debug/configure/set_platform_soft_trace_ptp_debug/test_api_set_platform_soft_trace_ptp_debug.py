import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.debug.configure import set_platform_soft_trace_ptp_debug


class TestSetPlatformSoftTracePtpDebug(TestCase):

    def test_set_platform_soft_trace_ptp_debug(self):
        device = Mock()
        result = set_platform_soft_trace_ptp_debug(device, 'fed', 'active', 'ptp_proto', 'debug', None)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify execute was called with the correct command
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('set platform software trace fed active ptp_proto debug',)
        )


if __name__ == '__main__':
    unittest.main()