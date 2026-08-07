from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    configure_smartpower_keywords,
)


class TestConfigureSmartpowerKeywords(TestCase):

    def test_configure_smartpower_keywords(self):
        device = Mock()

        result = configure_smartpower_keywords(device, 'tomato')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'smartpower keywords tomato'
        )
