import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_sensor.configure import configure_device_sensor_filter_spec


class TestConfigureDeviceSensorFilterSpec(TestCase):

    def test_configure_device_sensor_filter_spec(self):
        device = Mock()
        result = configure_device_sensor_filter_spec(device, 'cdp', True, False, 'all', None, 'TEST')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('device-sensor filter-spec cdp exclude all',)
        )


if __name__ == '__main__':
    unittest.main()