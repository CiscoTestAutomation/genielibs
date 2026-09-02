from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.udld.configure import (
    unconfigure_udld,
)


class TestUnconfigureUdld(TestCase):

    def test_unconfigure_udld(self):
        device = Mock()

        result = unconfigure_udld(device, 'aggressive')

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no udld aggressive')
