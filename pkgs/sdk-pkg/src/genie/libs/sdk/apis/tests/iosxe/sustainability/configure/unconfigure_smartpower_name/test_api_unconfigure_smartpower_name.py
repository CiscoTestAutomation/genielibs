from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_smartpower_name,
)


class TestUnconfigureSmartpowerName(TestCase):

    def test_unconfigure_smartpower_name(self):
        device = Mock()

        result = unconfigure_smartpower_name(device, 'abood')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no smartpower name abood')
