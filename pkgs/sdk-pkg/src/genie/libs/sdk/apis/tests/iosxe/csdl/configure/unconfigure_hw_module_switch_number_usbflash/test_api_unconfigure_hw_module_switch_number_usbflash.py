import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.configure import unconfigure_hw_module_switch_number_usbflash


class TestUnconfigureHwModuleSwitchNumberUsbflash(TestCase):

    def test_unconfigure_hw_module_switch_number_usbflash(self):
        device = Mock()
        result = unconfigure_hw_module_switch_number_usbflash(device, '1')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no hw-module switch 1 usbflash1-password'],)
        )


if __name__ == '__main__':
    unittest.main()