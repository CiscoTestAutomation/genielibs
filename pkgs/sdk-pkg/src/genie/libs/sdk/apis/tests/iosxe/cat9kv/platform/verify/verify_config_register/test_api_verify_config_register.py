import unittest
from unittest.mock import Mock
import logging
from genie.libs.sdk.apis.iosxe.cat9kv.platform.verify import verify_config_register


class TestVerifyConfigRegister(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        logging.getLogger().setLevel(logging.ERROR)

    def test_config_register_match_current(self):
        self.device.api.get_config_register.return_value = '0x2102'
        result = verify_config_register(self.device, '0x2102')
        self.assertTrue(result)

    def test_config_register_match_next_reload(self):
        self.device.api.get_config_register.return_value = '0x2101'
        result = verify_config_register(self.device, '0x2101', next_reload=True)
        self.assertTrue(result)

    def test_config_register_mismatch(self):
        self.device.api.get_config_register.return_value = '0x0'
        result = verify_config_register(self.device, '0x2102')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
