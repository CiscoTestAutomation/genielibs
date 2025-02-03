from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_device_parameters
from unittest.mock import Mock


class TestConfigureMacroAutoDeviceParameters(TestCase):

    def test_configure_macro_auto_device_parameters(self):
        self.device = Mock()
        result = configure_macro_auto_device_parameters(self.device, 'phone', 'ACCESS_VLAN=10 VOICE_VLAN=20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['macro auto device phone ACCESS_VLAN=10 VOICE_VLAN=20'],)
        )
