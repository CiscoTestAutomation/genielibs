from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sisf.configure import configure_vlan_config_device_tracking
from unittest.mock import Mock


class TestConfigureVlanConfigDeviceTracking(TestCase):

    def test_configure_vlan_config_device_tracking(self):
        self.device = Mock()
        result = configure_vlan_config_device_tracking(self.device, '50', None, '4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vlan configuration 50', 'device-tracking priority 4'],)
        )
