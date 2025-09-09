import unittest
from unittest.mock import Mock
import logging
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.cat9kv.platform.get import get_boot_variables


class TestGetBootVariables(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        logging.getLogger().setLevel(logging.ERROR)

    def test_get_current_boot_variable_from_current(self):
        self.device.parse.return_value = {
            'current_boot_variable': 'bootflash:iosxe-image.bin;'
        }
        result = get_boot_variables(self.device, 'current')
        self.assertEqual(result, ['bootflash:iosxe-image.bin'])

    def test_get_current_boot_variable_from_active(self):
        self.device.parse.return_value = {
            'active': {
                'boot_variable': 'bootflash:iosxe-active.bin;'
            }
        }
        result = get_boot_variables(self.device, 'current')
        self.assertEqual(result, ['bootflash:iosxe-active.bin'])

    def test_get_next_boot_variable_from_next_reload(self):
        self.device.parse.return_value = {
            'next_reload_boot_variable': 'bootflash:iosxe-next.bin;'
        }
        result = get_boot_variables(self.device, 'next')
        self.assertEqual(result, ['bootflash:iosxe-next.bin'])

    def test_get_next_boot_variable_from_active(self):
        self.device.parse.return_value = {
            'active': {
                'boot_variable': 'bootflash:iosxe-next-active.bin;'
            }
        }
        result = get_boot_variables(self.device, 'next')
        self.assertEqual(result, ['bootflash:iosxe-next-active.bin'])

    def test_get_boot_variable_multiple_values(self):
        self.device.parse.return_value = {
            'current_boot_variable': 'bootflash:image1.bin;bootflash:image2.bin;'
        }
        result = get_boot_variables(self.device, 'current')
        self.assertEqual(result, ['bootflash:image1.bin', 'bootflash:image2.bin'])

    def test_get_boot_variable_schema_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data returned")
        result = get_boot_variables(self.device, 'current')
        self.assertEqual(result, [])

    def test_invalid_boot_var_argument(self):
        with self.assertRaises(AssertionError):
            get_boot_variables(self.device, 'invalid')


if __name__ == '__main__':
    unittest.main()
