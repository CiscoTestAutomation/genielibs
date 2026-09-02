from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_smartpower_level,
)


class TestUnconfigureSmartpowerLevel(TestCase):

    def test_unconfigure_smartpower_level(self):
        device = Mock()

        result = unconfigure_smartpower_level(device, '1')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no smartpower level 1'
        )
