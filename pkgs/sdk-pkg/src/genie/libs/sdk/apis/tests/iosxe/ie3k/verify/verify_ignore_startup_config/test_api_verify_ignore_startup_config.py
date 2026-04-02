from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ie3k.verify import verify_ignore_startup_config


class TestVerifyIgnoreStartupConfig(TestCase):
    def test_verify_ignore_startup_config(self):
        device = Mock()
        device.execute = Mock()

        device.execute.return_value = 'MANUAL_BOOT = yes\nConfigReg = 0x142\nBSI = 0'
        result = verify_ignore_startup_config(device)
        device.execute.assert_called_with('show romvar')
        self.assertTrue(result)

        device.execute.return_value = 'MANUAL_BOOT = yes\nConfigReg = 0x102\nBSI = 0'
        result = verify_ignore_startup_config(device)
        device.execute.assert_called_with('show romvar')
        self.assertFalse(result)
