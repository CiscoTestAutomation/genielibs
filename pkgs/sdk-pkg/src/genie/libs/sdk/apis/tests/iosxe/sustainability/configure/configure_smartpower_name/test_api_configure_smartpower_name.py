from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_name,
)


class TestConfigureSmartpowerName(TestCase):

    def test_configure_smartpower_name(self):
        device = Mock()

        result = configure_smartpower_name(device, 'abood')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'smartpower name abood'
        )
