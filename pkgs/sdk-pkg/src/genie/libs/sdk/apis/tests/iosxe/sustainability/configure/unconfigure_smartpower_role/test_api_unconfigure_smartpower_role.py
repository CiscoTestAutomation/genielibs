from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sustainability.configure import (
    unconfigure_smartpower_role,
)


class TestUnconfigureSmartpowerRole(TestCase):

    def test_unconfigure_smartpower_role(self):
        device = Mock()

        result = unconfigure_smartpower_role(device, 'potato')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no smartpower role potato')
