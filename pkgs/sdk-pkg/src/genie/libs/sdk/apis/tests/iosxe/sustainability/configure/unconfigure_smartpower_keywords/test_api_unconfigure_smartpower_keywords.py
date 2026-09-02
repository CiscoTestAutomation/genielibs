from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_smartpower_keywords,
)


class TestUnconfigureSmartpowerKeywords(TestCase):

    def test_unconfigure_smartpower_keywords(self):
        device = Mock()

        result = unconfigure_smartpower_keywords(device, 'tomato')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no smartpower keywords tomato'
        )
