from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.traceroute.configure import (
    configure_l2_traceroute,
)


class TestConfigureL2Traceroute(TestCase):

    def test_configure_l2_traceroute(self):
        device = Mock()

        result = configure_l2_traceroute(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('l2 traceroute')
