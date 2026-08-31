from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.telemetry.configure import (
    configure_netconf_yang,
)


class TestConfigureNetconfYang(TestCase):

    def test_configure_netconf_yang(self):
        device = Mock()

        result = configure_netconf_yang(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('netconf-yang')
