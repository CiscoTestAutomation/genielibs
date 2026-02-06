from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.configure import configure_hw_module_switch_number_usbflash


class TestConfigureHwModuleSwitchNumberUsbflash(TestCase):
    def test_configure_hw_module_switch_number_usbflash(self):
        device = Mock()
        result = configure_hw_module_switch_number_usbflash(device, '1', '123456789')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['hw-module switch 1 usbflash1-password 123456789'],)
        )