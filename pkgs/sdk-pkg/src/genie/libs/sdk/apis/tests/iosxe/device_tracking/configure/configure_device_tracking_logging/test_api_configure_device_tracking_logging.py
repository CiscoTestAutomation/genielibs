import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_tracking.configure import configure_device_tracking_logging


class TestConfigureDeviceTrackingLogging(TestCase):

    def test_configure_device_tracking_logging(self):
        device = Mock()
        result = configure_device_tracking_logging(device, 'packet')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('device-tracking logging packet drop',)
        )


if __name__ == '__main__':
    unittest.main()