from unittest import TestCase
from genie.libs.sdk.apis.iosxe.device_sensor.configure import unconfigure_device_sensor_dhcpv6_snooping
from unittest.mock import Mock


class TestUnconfigureDeviceSensorDhcpv6Snooping(TestCase):

    def test_unconfigure_device_sensor_dhcpv6_snooping(self):
        self.device = Mock()
        result = unconfigure_device_sensor_dhcpv6_snooping(self.device, 'FiveGigabitEthernet4/0/4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface FiveGigabitEthernet4/0/4', 'no device-sensor dhcpv6-snooping'],)
        )
