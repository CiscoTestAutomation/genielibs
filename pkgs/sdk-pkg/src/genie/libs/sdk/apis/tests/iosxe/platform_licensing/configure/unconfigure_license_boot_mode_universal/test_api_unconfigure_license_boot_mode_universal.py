from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import unconfigure_license_boot_mode_universal
from unittest.mock import Mock


class TestUnconfigureLicenseBootModeUniversal(TestCase):

    def test_unconfigure_license_boot_mode_universal(self):
        self.device = Mock()
        result = unconfigure_license_boot_mode_universal(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no license boot mode universal',)
        )
