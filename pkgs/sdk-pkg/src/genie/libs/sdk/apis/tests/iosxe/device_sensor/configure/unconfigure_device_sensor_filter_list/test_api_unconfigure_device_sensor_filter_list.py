import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.device_sensor.configure import unconfigure_device_sensor_filter_list


class TestUnconfigureDeviceSensorFilterList(TestCase):

    def test_unconfigure_device_sensor_filter_list(self):
        device = Mock()
        result = unconfigure_device_sensor_filter_list(device, 'cdp', 'lisds', 'device-name', None, None, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['device-sensor filter-list cdp list lisds', 'no tlv name device-name'],)
        )


if __name__ == '__main__':
    unittest.main()