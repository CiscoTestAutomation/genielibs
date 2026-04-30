import unittest
from unittest.mock import Mock
from unittest.mock import call
from genie.libs.sdk.apis.iosxe.ie3k.rommon.get import get_recovery_details


class TestGetRecoveryDetails(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-IE3K"
        self.device.settings.BOOT_FILESYSTEM = ['flash:', 'sdflash:']

    def test_provided_golden_image(self):
        """Verify provided golden_image is used without searching filesystems."""
        provided_image = ['flash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260407_003317.SSA.bin']
        
        result = get_recovery_details(self.device, golden_image=provided_image)

        expected = {
            'golden_image': ['flash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260407_003317.SSA.bin']
        }
        
        self.assertEqual(result, expected)
        # Verify device.execute was NOT called since image was provided
        self.device.execute.assert_not_called()

    def test_no_image(self):
        """Verify an empty golden_image list is returned when no image is found."""
        empty_output = """
 Date       Time    Attribute   Size         Name

 ========== =====   ==========  ==========   ================

 2026/02/03 05:49   drwxr-xr-x        4096   .product_analytics

 2026/04/16 17:10   -rw-rw-rw-       38857   show_tech_support_20260416T114019554.txt

 2025/08/14 14:48   drwx------        4096   yang-infra
"""
        self.device.execute.side_effect = [empty_output, empty_output]

        result = get_recovery_details(self.device)

        self.assertEqual(result, {'golden_image': []})
        self.assertEqual(self.device.execute.call_count, 2)

    def test_multiple_images(self):
        """Verify all matching images are returned in filesystem order."""
        flash_output = """
Date       Time    Attribute   Size         Name

========== =====   ==========  ==========   ================

2026/04/18 15:36   -rw-r--r--    18567876   ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260407_003317.SSA.bin
2026/04/17 09:06   -rw-r--r--    19753161   ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260404_033234_V26_2_0_38.SSA.bin
"""
        sdflash_output = """
Date       Time    Attribute   Size         Name

========== =====   ==========  ==========   ================

2026/04/18 15:21   -rw-rw-rw-  463552123    ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260416_003353.SSA.bin
"""
        self.device.execute.side_effect = [flash_output, sdflash_output]

        result = get_recovery_details(self.device)

        expected = {
            'golden_image': [
                'flash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260407_003317.SSA.bin',
                'flash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260404_033234_V26_2_0_38.SSA.bin',
                'sdflash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260416_003353.SSA.bin'
            ]
        }

        self.assertEqual(result, expected)
        self.device.execute.assert_has_calls([call('dir flash:'), call('dir sdflash:')])
        self.assertEqual(self.device.execute.call_count, 2)

    def test_tftp_ignored(self):
        """Verify tftp_boot parameter is ignored (IE3K does not support TFTP boot in ROMMON)."""
        self.device.execute.side_effect = ["""
Date       Time    Attribute   Size         Name

========== =====   ==========  ==========   ================

2026/04/18 15:36   -rw-r--r--  18567876     ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260404_033234_V26_2_0_38.SSA.bin

    Total space = 1684480 KB

    Available   = 466516 KB
""", "Directory of sdflash:/\n\n"]

        tftp_boot = {
            'image': ['ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260407_003317.SSA.bin'],
            'tftp_server': '10.1.1.1'
        }

        result = get_recovery_details(self.device, tftp_boot=tftp_boot)

        # TFTP info should NOT appear in result for IE3K
        expected = {
            'golden_image': ['flash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260404_033234_V26_2_0_38.SSA.bin']
        }

        self.assertEqual(result, expected)
        self.assertNotIn('tftp_boot', result)
        self.assertNotIn('tftp_image', result)
