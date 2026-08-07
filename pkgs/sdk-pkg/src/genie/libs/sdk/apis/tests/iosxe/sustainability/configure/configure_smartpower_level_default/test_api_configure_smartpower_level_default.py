from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_level_default,
)


class TestConfigureSmartpowerLevelDefault(TestCase):

    def test_configure_smartpower_level_default(self):
        device = Mock()

        result = configure_smartpower_level_default(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'default smartpower level'
        )
