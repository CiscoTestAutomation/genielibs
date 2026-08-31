from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_smartpower_importance,
)


class TestUnconfigureSmartpowerImportance(TestCase):

    def test_unconfigure_smartpower_importance(self):
        device = Mock()

        result = unconfigure_smartpower_importance(device, '5')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no smartpower importance 5'
        )
