import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_sensor.configure import configure_device_sensor_filter_list


class TestConfigureDeviceSensorFilterList(TestCase):

    def test_configure_device_sensor_filter_list(self):
        device = Mock()
        result = configure_device_sensor_filter_list(device, 'cdp', 'cdp_test', None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['device-sensor filter-list cdp list cdp_test'],)
        )


if __name__ == '__main__':
    unittest.main()