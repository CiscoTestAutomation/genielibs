from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_mac_address_group
from unittest.mock import Mock


class TestUnconfigureMacroAutoMacAddressGroup(TestCase):

    def test_unconfigure_macro_auto_mac_address_group(self):
        self.device = Mock()
        result = unconfigure_macro_auto_mac_address_group(self.device, 'triiger_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no macro auto mac-address-group triiger_1',)
        )
