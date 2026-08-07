from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_level,
)


class TestConfigureSmartpowerLevel(TestCase):

    def test_configure_smartpower_level(self):
        device = Mock()

        result = configure_smartpower_level(device, '1')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'smartpower level 1'
        )
