import unittest
from unittest.mock import Mock
import logging
from genie.libs.sdk.apis.iosxe.cat9kv.platform.verify import verify_boot_variable


class TestVerifyBootVariable(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        logging.getLogger().setLevel(logging.ERROR)

    def test_boot_variables_match_exact(self):
        self.device.api.get_boot_variables.return_value = [
            'bootflash:image1.bin', 'bootflash:image2.bin'
        ]
        result = verify_boot_variable(
            self.device, ['bootflash:image1.bin', 'bootflash:image2.bin'])
        self.assertTrue(result)

    def test_boot_variables_match_with_flash_prefix(self):
        self.device.api.get_boot_variables.return_value = [
            'flash:image1.bin', 'bootflash:image2.bin'
        ]
        result = verify_boot_variable(
            self.device, ['bootflash:image1.bin', 'flash:image2.bin'])
        self.assertTrue(result)

    def test_boot_variables_mismatch_in_value(self):
        self.device.api.get_boot_variables.return_value = [
            'bootflash:image1.bin', 'bootflash:image3.bin'
        ]
        result = verify_boot_variable(
            self.device, ['bootflash:image1.bin', 'bootflash:image2.bin'])
        self.assertFalse(result)

    def test_boot_variables_mismatch_in_length(self):
        self.device.api.get_boot_variables.return_value = [
            'bootflash:image1.bin'
        ]
        result = verify_boot_variable(
            self.device, ['bootflash:image1.bin', 'bootflash:image2.bin'])
        self.assertFalse(result)

    def test_boot_variables_directory_ignore_fail(self):
        self.device.api.get_boot_variables.return_value = [
            'bootflash:image1.bin', 'flash:image3.bin'
        ]
        result = verify_boot_variable(
            self.device, ['bootflash:image1.bin', 'bootflash:image2.bin'])
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
