import unittest
from unittest.mock import Mock
import logging
from genie.libs.sdk.apis.iosxe.cat9kv.platform.get import get_config_register


class TestGetConfigRegister(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        logging.getLogger().setLevel(logging.ERROR)

    def test_get_current_config_register(self):
        self.device.parse.return_value = {
            'version': {
                'curr_config_register': '0x2102'
            }
        }
        result = get_config_register(self.device)
        self.assertEqual(result, '0x2102')

    def test_get_next_config_register(self):
        self.device.parse.return_value = {
            'version': {
                'next_config_register': '0x0',
                'curr_config_register': '0x2102'
            }
        }
        result = get_config_register(self.device, next_reload=True)
        self.assertEqual(result, '0x0')

    def test_get_next_config_register_fallback_to_current(self):
        self.device.parse.return_value = {
            'version': {
                'curr_config_register': '0x2101'
            }
        }
        result = get_config_register(self.device, next_reload=True)
        self.assertEqual(result, '0x2101')

    def test_get_config_register_key_missing(self):
        self.device.parse.return_value = {
            'version': {}
        }
        result = get_config_register(self.device)
        self.assertIsNone(result)

    def test_get_config_register_no_version_key(self):
        self.device.parse.return_value = {
            'curr_config_register': '0x2102'
        }
        result = get_config_register(self.device)
        self.assertEqual(result, '0x2102')

    def test_parse_command_fails(self):
        self.device.parse.side_effect = Exception("Parse failed")
        result = get_config_register(self.device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
