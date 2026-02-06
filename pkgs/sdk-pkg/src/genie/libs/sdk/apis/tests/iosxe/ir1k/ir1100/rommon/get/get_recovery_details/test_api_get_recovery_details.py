import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ir1k.ir1100.rommon.get import get_recovery_details


class TestGetRecoveryDetailsUsbflash(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-IR1100"
        
        # Mock output for dir usbflash0: with a golden image
        self.device.execute.return_value = """
Directory of usbflash0:/

    1  -rw-   536870912  Jan 15 2025 10:30:00 +00:00  ir1101-universalk9.BLD_V1712_THROTTLE_LATEST_20250115_100327_V17_12_0_141.bin
    2  -rw-     1024      Jan 10 2025 08:15:00 +00:00  config.txt

7864320 bytes total (7327232 bytes free)
"""

    def test_get_recovery_details_usbflash(self):
        """Verify golden image is found in usbflash0:."""
        result = get_recovery_details(self.device)

        expected = {
            'golden_image': ['usbflash0:ir1101-universalk9.BLD_V1712_THROTTLE_LATEST_20250115_100327_V17_12_0_141.bin']
        }
        
        self.assertEqual(result, expected)
        self.device.execute.assert_called_once_with('dir usbflash0:')


class TestGetRecoveryDetailsBootflash(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-IR1100"

    def test_get_recovery_details_bootflash(self):
        """Verify golden image is found in bootflash: when not in usbflash0:."""
        # Mock: usbflash0: has no matching images, bootflash: has one
        usbflash_output = """
Directory of usbflash0:/

    1  -rw-     1024      Jan 10 2025 08:15:00 +00:00  config.txt

7864320 bytes total (7863296 bytes free)
"""
        bootflash_output = """
Directory of bootflash:/

    1  -rw-   536870912  Jan 12 2025 14:22:00 +00:00  ir1101-universalk9.BLD_V1712_THROTTLE_LATEST_20250112_142200_V17_12_0_140.bin
    2  -rw-     2048      Jan 11 2025 10:00:00 +00:00  startup-config

1048576000 bytes total (511705088 bytes free)
"""
        self.device.execute.side_effect = [usbflash_output, bootflash_output]

        result = get_recovery_details(self.device)

        expected = {
            'golden_image': ['bootflash:ir1101-universalk9.BLD_V1712_THROTTLE_LATEST_20250112_142200_V17_12_0_140.bin']
        }
        
        self.assertEqual(result, expected)
        self.assertEqual(self.device.execute.call_count, 2)


class TestGetRecoveryDetailsProvidedImage(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-IR1100"

    def test_get_recovery_details_provided_image(self):
        """Verify provided golden_image is used without searching filesystems."""
        provided_image = ['usbflash0:ir1101-universalk9.BLD_CUSTOM_IMAGE.bin']
        
        result = get_recovery_details(self.device, golden_image=provided_image)

        expected = {
            'golden_image': ['usbflash0:ir1101-universalk9.BLD_CUSTOM_IMAGE.bin']
        }
        
        self.assertEqual(result, expected)
        # Verify device.execute was NOT called since image was provided
        self.device.execute.assert_not_called()


class TestGetRecoveryDetailsNoImage(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-IR1100"

    def test_get_recovery_details_no_image(self):
        """Verify exception is raised when no golden image is found."""
        # Mock: neither usbflash0: nor bootflash: have matching images
        empty_usbflash = """
Directory of usbflash0:/

    1  -rw-     1024      Jan 10 2025 08:15:00 +00:00  config.txt

7864320 bytes total (7863296 bytes free)
"""
        empty_bootflash = """
Directory of bootflash:/

    1  -rw-     2048      Jan 11 2025 10:00:00 +00:00  startup-config
    2  -rw-     4096      Jan 09 2025 09:30:00 +00:00  some-other-file.txt

1048576000 bytes total (1048569856 bytes free)
"""
        self.device.execute.side_effect = [empty_usbflash, empty_bootflash]

        with self.assertRaises(Exception) as context:
            get_recovery_details(self.device)
        
        self.assertIn("No golden image found", str(context.exception))
        self.assertEqual(self.device.execute.call_count, 2)


class TestGetRecoveryDetailsTftpIgnored(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-IR1100"
        
        self.device.execute.return_value = """
Directory of usbflash0:/

    1  -rw-   536870912  Jan 15 2025 10:30:00 +00:00  ir1101-universalk9.BLD_V1712_THROTTLE_LATEST_20250115_100327_V17_12_0_141.bin

7864320 bytes total (7327232 bytes free)
"""

    def test_get_recovery_details_tftp_ignored(self):
        """Verify tftp_boot parameter is ignored (IR1100 does not support TFTP boot in ROMMON)."""
        tftp_boot = {
            'image': ['ir1101-universalk9.bin'],
            'tftp_server': '10.1.1.1'
        }
        
        result = get_recovery_details(self.device, tftp_boot=tftp_boot)

        # TFTP info should NOT appear in result for IR1100
        expected = {
            'golden_image': ['usbflash0:ir1101-universalk9.BLD_V1712_THROTTLE_LATEST_20250115_100327_V17_12_0_141.bin']
        }
        
        self.assertEqual(result, expected)
        self.assertNotIn('tftp_boot', result)
        self.assertNotIn('tftp_image', result)
