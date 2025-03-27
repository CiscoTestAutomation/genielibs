from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_boot_system_switch_all_flash
from unittest.mock import Mock


class TestUnconfigureBootSystemSwitchAllFlash(TestCase):

    def test_unconfigure_boot_system_switch_all_flash(self):
        self.device = Mock()
        result = unconfigure_boot_system_switch_all_flash(self.device, 'testAll')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no boot system switch all flash:testAll',)
        )
