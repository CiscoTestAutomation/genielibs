from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sisf.configure import configure_device_tracking_binding_globally
from unittest.mock import Mock


class TestConfigureDeviceTrackingBindingGlobally(TestCase):

    def test_configure_device_tracking_binding_globally(self):
        self.device = Mock()
        result = configure_device_tracking_binding_globally(self.device, '88', '1.1.1.1', 'GigabitEthernet1/0/1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('device-tracking binding vlan 88 1.1.1.1 interface GigabitEthernet1/0/1',)
        )
