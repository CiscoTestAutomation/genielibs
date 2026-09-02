from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    unconfigure_netconf_yang,
)


class TestUnconfigureNetconfYang(TestCase):

    def test_unconfigure_netconf_yang(self):
        device = Mock()

        result = unconfigure_netconf_yang(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no netconf-yang')
