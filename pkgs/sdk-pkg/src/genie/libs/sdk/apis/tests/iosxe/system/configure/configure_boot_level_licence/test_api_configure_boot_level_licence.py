from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.system.configure import (
    configure_boot_level_licence,
)


class TestConfigureBootLevelLicence(TestCase):

    def test_configure_boot_level_licence(self):
        device = Mock()

        result = configure_boot_level_licence(
            device,
            advantage=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with('license boot level advantage')

    def test_configure_boot_level_licence_1(self):
        device = Mock()

        result = configure_boot_level_licence(
            device,
            essentials=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'license boot level essentials'
        )
