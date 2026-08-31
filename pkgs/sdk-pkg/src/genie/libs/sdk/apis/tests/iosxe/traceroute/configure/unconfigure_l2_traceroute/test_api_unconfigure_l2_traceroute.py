from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.traceroute.configure import (
    unconfigure_l2_traceroute,
)


class TestUnconfigureL2Traceroute(TestCase):

    def test_unconfigure_l2_traceroute(self):
        device = Mock()

        result = unconfigure_l2_traceroute(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no l2 traceroute')
