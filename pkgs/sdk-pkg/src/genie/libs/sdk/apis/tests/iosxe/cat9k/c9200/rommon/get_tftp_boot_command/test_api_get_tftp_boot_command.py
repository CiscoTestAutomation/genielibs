import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9200.rommon.get import get_tftp_boot_command


class TestGetTftpBootCommand(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-C9200"
        self.recovery_info = {
            'tftp_boot': {
                'tftp_server': '15.11.20.02',
                'image': ['cat9k_iosxe.16.12.1.SPA.bin']
            }
        }

    def test_get_tftp_boot_command_success(self):
        """Verify correct full URL and image when TFTP info is present."""
        cmd, image = get_tftp_boot_command(self.device, self.recovery_info)

        expected_cmd = "tftp://15.11.20.02/cat9k_iosxe.16.12.1.SPA.bin"
        expected_image = "cat9k_iosxe.16.12.1.SPA.bin"

        self.assertEqual(cmd, expected_cmd)
        self.assertEqual(image, expected_image)

    def test_get_tftp_boot_command_missing_info(self):
        """Verify exception raised when TFTP info is missing."""
        self.recovery_info = {'tftp_boot': {}}
        with self.assertRaises(Exception):
            get_tftp_boot_command(self.device, self.recovery_info)