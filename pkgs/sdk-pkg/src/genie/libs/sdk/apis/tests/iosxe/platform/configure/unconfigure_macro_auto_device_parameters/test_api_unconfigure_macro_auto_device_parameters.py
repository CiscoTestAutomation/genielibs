from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_device_parameters
from unittest.mock import Mock


class TestUnconfigureMacroAutoDeviceParameters(TestCase):

    def test_unconfigure_macro_auto_device_parameters(self):
        self.device = Mock()
        result = unconfigure_macro_auto_device_parameters(self.device, 'phone', 'ACCESS_VLAN=10 VOICE_VLAN=20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no macro auto device phone ACCESS_VLAN=10 VOICE_VLAN=20'],)
        )
