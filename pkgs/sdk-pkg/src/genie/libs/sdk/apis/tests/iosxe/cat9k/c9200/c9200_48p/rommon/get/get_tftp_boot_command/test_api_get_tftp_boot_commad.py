import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9200.c9200_48p.rommon.get import get_tftp_boot_command


class TestGetTftpBootCommand(unittest.TestCase):

    def setUp(self):
        # Mock device
        self.device = Mock()
        self.device.name = "Mock-C9200-48P"
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