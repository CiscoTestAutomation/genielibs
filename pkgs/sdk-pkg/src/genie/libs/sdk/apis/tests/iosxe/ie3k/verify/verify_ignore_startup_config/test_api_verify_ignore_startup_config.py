import unittest
from unittest import mock
from genie.libs.sdk.apis.iosxe.ie3k.verify import verify_ignore_startup_config


class TestVerifyIgnoreStartupConfig(unittest.TestCase):

    def setUp(self):
        self.device = mock.Mock()
        self.device.name = 'ie3k-device'

    # --- ConfigReg path ---

    def test_confreg_ignore_bit_set_returns_true(self):
        # 0x40 has bit 6 set
        self.device.execute.return_value = "ConfigReg = 0x40"
        self.assertTrue(verify_ignore_startup_config(self.device))

    def test_confreg_invalid_hex_raises_value_error(self):
        self.device.execute.return_value = "ConfigReg = 0xGGGG"
        with self.assertRaises(ValueError):
            verify_ignore_startup_config(self.device)

    def test_switch_ignore_startup_cfg_1_returns_true(self):
        self.device.execute.return_value = "SWITCH_IGNORE_STARTUP_CFG = 1"
        self.assertTrue(verify_ignore_startup_config(self.device))

    def test_switch_ignore_startup_cfg_0_returns_false(self):
        self.device.execute.return_value = "SWITCH_IGNORE_STARTUP_CFG = 0"
        self.assertFalse(verify_ignore_startup_config(self.device))


if __name__ == '__main__':
    unittest.main()
