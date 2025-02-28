from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sisf.configure import unconfigure_device_tracking_binding_globally
from unittest.mock import Mock


class TestUnconfigureDeviceTrackingBindingGlobally(TestCase):

    def test_unconfigure_device_tracking_binding_globally(self):
        self.device = Mock()
        result = unconfigure_device_tracking_binding_globally(self.device, '88', '1.1.1.1', 'GigabitEthernet1/0/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no device-tracking binding vlan 88 1.1.1.1 interface GigabitEthernet1/0/1',)
        )
