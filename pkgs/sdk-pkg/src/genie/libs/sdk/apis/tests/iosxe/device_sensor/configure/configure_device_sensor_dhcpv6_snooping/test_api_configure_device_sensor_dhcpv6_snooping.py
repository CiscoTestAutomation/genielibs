from unittest import TestCase
from genie.libs.sdk.apis.iosxe.device_sensor.configure import configure_device_sensor_dhcpv6_snooping
from unittest.mock import Mock


class TestConfigureDeviceSensorDhcpv6Snooping(TestCase):

    def test_configure_device_sensor_dhcpv6_snooping(self):
        self.device = Mock()
        result = configure_device_sensor_dhcpv6_snooping(self.device, 'FiveGigabitEthernet4/0/4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface FiveGigabitEthernet4/0/4', 'device-sensor dhcpv6-snooping'],)
        )
