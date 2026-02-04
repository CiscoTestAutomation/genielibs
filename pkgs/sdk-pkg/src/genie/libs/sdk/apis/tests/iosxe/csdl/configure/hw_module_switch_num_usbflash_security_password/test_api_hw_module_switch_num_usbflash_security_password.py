from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.configure import hw_module_switch_num_usbflash_security_password


class TestHwModuleSwitchNumUsbflashSecurityPassword(TestCase):
    def test_hw_module_switch_num_usbflash_security_password(self):
        device = Mock()
        result = hw_module_switch_num_usbflash_security_password(device, '1', 'enable', '123456')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['hw-module switch 1 usbflash1 security enable password 123456'],)
        )