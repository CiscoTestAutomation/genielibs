from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_mac_address_group
from unittest.mock import Mock


class TestConfigureMacroAutoMacAddressGroup(TestCase):

    def test_configure_macro_auto_mac_address_group(self):
        self.device = Mock()
        result = configure_macro_auto_mac_address_group(self.device, 'test_add', 'mac-address', '1111.2222.3333')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['macro auto mac-address-group test_add', 'mac-address list 1111.2222.3333'],)
        )
