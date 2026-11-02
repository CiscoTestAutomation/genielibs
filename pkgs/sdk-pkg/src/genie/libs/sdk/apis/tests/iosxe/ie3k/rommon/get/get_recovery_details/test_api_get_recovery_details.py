import unittest
from types import SimpleNamespace
from unittest.mock import Mock
from unittest.mock import call
from genie.libs.sdk.apis.iosxe.ie3k.rommon.get import get_recovery_details


class TestGetRecoveryDetails(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-IE3K"
        self.device.settings = SimpleNamespace(
            EMERGENCY_FILESYSTEMS=['emgy:', 'emgy0:'],
            EMERGENCY_IMAGE_PATTERN=r'(\d+)\s+(\S+\.bin)',
            BOOT_FILESYSTEM=['flash:', 'sdflash:'],
            BOOT_FILE_REGEX=[
                r'(\S+\.SSA\.bin)',
                r'(\S+\.SPA\.bin)',
                r'(\S+\.bin)',
            ],
        )
        self.device.clean = {}
        self.empty_output = "Directory is empty"

    def test_provided_golden_image(self):
        """Verify emergency images precede a provided golden_image."""
        provided_image = ['sdflash:golden_image.bin']
        self.device.execute.side_effect = [
            "-rw-r--r--  1234  emergency.bin",
            self.empty_output,
            "-rw-r--r--  2345  flash_image.SSA.bin",
            "-rw-r--r--  3456  sd_image.SSA.bin",
        ]

        result = get_recovery_details(self.device, golden_image=provided_image)

        expected = {
            'golden_image': [
                'emgy:emergency.bin',
                'sdflash:golden_image.bin',
                'flash:flash_image.SSA.bin',
                'sdflash:sd_image.SSA.bin',
            ]
        }

        self.assertEqual(result, expected)
        self.device.execute.assert_has_calls([
            call('dir emgy:', timeout=600),
            call('dir emgy0:', timeout=600),
            call('dir flash:', timeout=600),
            call('dir sdflash:', timeout=600),
        ])
        self.assertEqual(self.device.execute.call_count, 4)

    def test_provided_golden_image_without_emergency_is_unchanged(self):
        """Keep a scalar supplied image as the only recovery candidate."""
        provided_image = 'sdflash:golden_image.bin'
        self.device.execute.side_effect = [self.empty_output] * 4

        result = get_recovery_details(self.device, golden_image=provided_image)

        self.assertEqual(result, {'golden_image': [provided_image]})
        self.assertEqual(self.device.execute.call_count, 4)

    def test_clean_recovery_image_precedes_boot_filesystem_images(self):
        """Use Clean's recovery image before the configured filesystem order."""
        self.device.clean = {
            'device_recovery': {
                'golden_image': ['sdflash:golden_image.bin'],
            },
        }
        self.device.execute.side_effect = [
            self.empty_output,
            self.empty_output,
            "-rw-r--r--  2345  fallback.SPA.bin",
            "-rw-r--r--  3456  preferred.SSA.bin\n"
            "-rw-r--r--  4567  golden_image.bin",
        ]

        result = get_recovery_details(self.device)

        self.assertEqual(result, {
            'golden_image': [
                'sdflash:golden_image.bin',
                'sdflash:preferred.SSA.bin',
                'flash:fallback.SPA.bin',
            ],
        })

    def test_explicit_golden_image_overrides_clean_recovery_image(self):
        """An explicit API argument remains the configured-image override."""
        self.device.clean = {
            'device_recovery': {
                'golden_image': ['sdflash:clean_golden.bin'],
            },
        }
        self.device.execute.side_effect = [self.empty_output] * 4

        result = get_recovery_details(
            self.device, golden_image='flash:explicit_golden.bin')

        self.assertEqual(result, {
            'golden_image': ['flash:explicit_golden.bin'],
        })

    def test_boot_file_regex_priority_applies_across_filesystems(self):
        """Preserve the platform's regex priority before filesystem order."""
        self.device.execute.side_effect = [
            self.empty_output,
            self.empty_output,
            "-rw-r--r--  1234  flash_fallback.bin\n"
            "-rw-r--r--  2345  flash_preferred.SPA.bin",
            "-rw-r--r--  3456  sdflash_preferred.SSA.bin\n"
            "-rw-r--r--  4567  sdflash_fallback.bin",
        ]

        result = get_recovery_details(self.device)

        self.assertEqual(result, {
            'golden_image': [
                'sdflash:sdflash_preferred.SSA.bin',
                'flash:flash_preferred.SPA.bin',
                'flash:flash_fallback.bin',
                'sdflash:sdflash_fallback.bin',
            ],
        })

    def test_no_image(self):
        """Verify an empty golden_image list is returned when no image is found."""
        empty_output = """
 Date       Time    Attribute   Size         Name

 ========== =====   ==========  ==========   ================

 2026/02/03 05:49   drwxr-xr-x        4096   .product_analytics

 2026/04/16 17:10   -rw-rw-rw-       38857   show_tech_support_20260416T114019554.txt

 2025/08/14 14:48   drwx------        4096   yang-infra
"""
        self.device.execute.side_effect = [empty_output] * 4

        result = get_recovery_details(self.device)

        self.assertEqual(result, {'golden_image': []})
        self.assertEqual(self.device.execute.call_count, 4)

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
        self.device.execute.side_effect = [
            self.empty_output,
            self.empty_output,
            flash_output,
            sdflash_output,
        ]

        result = get_recovery_details(self.device)

        expected = {
            'golden_image': [
                'flash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260407_003317.SSA.bin',
                'flash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260404_033234_V26_2_0_38.SSA.bin',
                'sdflash:ie35xx-universalk9.BLD_POLARIS_DEV_LATEST_20260416_003353.SSA.bin'
            ]
        }

        self.assertEqual(result, expected)
        self.device.execute.assert_has_calls([
            call('dir emgy:', timeout=600),
            call('dir emgy0:', timeout=600),
            call('dir flash:', timeout=600),
            call('dir sdflash:', timeout=600),
        ])
        self.assertEqual(self.device.execute.call_count, 4)

    def test_tftp_ignored(self):
        """Verify tftp_boot parameter is ignored (IE3K does not support TFTP boot in ROMMON)."""
        self.device.execute.side_effect = [self.empty_output, self.empty_output, """
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

    def test_emergency_and_ssa_order(self):
        """Emergency images precede normal SSA fallbacks."""
        self.device.execute.side_effect = [
            "-rw-r--r--  1234  emergency.bin",
            "-rw-r--r--  2345  alternate.SSA.bin",
            "-rw-r--r--  3456  flash_image.SSA.bin",
            "-rw-r--r--  4567  sd_image.SSA.bin",
        ]

        result = get_recovery_details(self.device)

        self.assertEqual(result, {
            'golden_image': [
                'emgy:emergency.bin',
                'emgy0:alternate.SSA.bin',
                'flash:flash_image.SSA.bin',
                'sdflash:sd_image.SSA.bin',
            ],
        })

    def test_missing_emgy_filesystem_does_not_skip_emgy0(self):
        """Probe the alternate emergency filesystem when emgy is absent."""
        self.device.execute.side_effect = [
            "Error: unknown filesystem\nrommon>",
            "-rw-r--r--  2345  emergency.bin",
            self.empty_output,
            self.empty_output,
        ]

        result = get_recovery_details(self.device)

        self.assertEqual(result, {
            'golden_image': ['emgy0:emergency.bin'],
        })

    def test_zero_size_images_are_not_returned(self):
        self.device.execute.side_effect = [
            "-rw-r--r--  0  empty.bin",
            self.empty_output,
            "-rw-r--r--  0  empty.SSA.bin",
            self.empty_output,
        ]

        result = get_recovery_details(self.device)

        self.assertEqual(result, {'golden_image': []})
