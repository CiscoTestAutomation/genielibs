from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_license_boot_mode_universal
from unittest.mock import Mock


class TestConfigureLicenseBootModeUniversal(TestCase):

    def test_configure_license_boot_mode_universal(self):
        self.device = Mock()
        result = configure_license_boot_mode_universal(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('license boot mode universal',)
        )
