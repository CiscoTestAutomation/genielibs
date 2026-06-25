from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_license_boot_mode
from unittest.mock import Mock


class TestUnconfigureLicenseBootMode(TestCase):

    def test_unconfigure_license_boot_mode(self):
        self.device = Mock()
        result = unconfigure_license_boot_mode(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no license boot mode',)
        )
