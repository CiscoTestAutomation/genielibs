from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_name_default,
)


class TestConfigureSmartpowerNameDefault(TestCase):

    def test_configure_smartpower_name_default(self):
        device = Mock()

        result = configure_smartpower_name_default(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'default smartpower name'
        )
