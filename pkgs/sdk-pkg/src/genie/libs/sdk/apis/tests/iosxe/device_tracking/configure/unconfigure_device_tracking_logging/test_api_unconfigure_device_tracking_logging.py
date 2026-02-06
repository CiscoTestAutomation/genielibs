import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_tracking.configure import unconfigure_device_tracking_logging


class TestUnconfigureDeviceTrackingLogging(TestCase):

    def test_unconfigure_device_tracking_logging(self):
        device = Mock()
        result = unconfigure_device_tracking_logging(device, 'packet')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no device-tracking logging packet drop',)
        )


if __name__ == '__main__':
    unittest.main()