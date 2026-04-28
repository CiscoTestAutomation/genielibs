from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_boot_system_switch_switchnumber


class TestConfigureBootSystemSwitchSwitchnumber(TestCase):

    def test_configure_boot_system_switch_switchnumber(self):
        device = Mock()
        result = configure_boot_system_switch_switchnumber(
            device,
            1,
            'flash:'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('boot system switch 1 flash:',)
        )