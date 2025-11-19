import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.rommon.get import get_tftp_boot_command


class TestIosxeRommonGetTftpBootCommand(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock"

    def test_tftp_command(self):
        recovery_info = {
            'tftp_boot': {
                'image': ['iosxe_image.bin']
            }
        }
        cmd, image = get_tftp_boot_command(self.device, recovery_info)
        self.assertEqual(cmd, "tftp:")
        self.assertEqual(image, "iosxe_image.bin")

