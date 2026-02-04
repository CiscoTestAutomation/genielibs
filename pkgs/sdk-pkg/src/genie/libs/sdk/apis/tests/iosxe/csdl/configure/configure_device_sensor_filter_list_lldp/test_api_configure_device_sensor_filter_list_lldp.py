from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.configure import configure_device_sensor_filter_list_lldp


class TestConfigureDeviceSensorFilterListLldp(TestCase):
    def test_configure_device_sensor_filter_list_lldp(self):
        device = Mock()
        result = configure_device_sensor_filter_list_lldp(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'device-sensor filter-list lldp list system-name',
                'device-sensor filter-list lldp list system-description',
                'device-sensor filter-list lldp list system-capabilities'
            ],)
        )