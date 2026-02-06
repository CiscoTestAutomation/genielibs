import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_sensor.configure import configure_device_sensor_notify


class TestConfigureDeviceSensorNotify(TestCase):

    def test_configure_device_sensor_notify(self):
        device = Mock()
        result = configure_device_sensor_notify(device, 'all-changes')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('device-sensor notify all-changes',)
        )


if __name__ == '__main__':
    unittest.main()