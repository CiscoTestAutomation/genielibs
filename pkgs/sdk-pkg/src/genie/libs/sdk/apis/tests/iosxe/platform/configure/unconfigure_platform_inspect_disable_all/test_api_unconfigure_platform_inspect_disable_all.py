from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import (
    unconfigure_platform_inspect_disable_all,
)


class TestUnconfigurePlatformInspectDisableAll(TestCase):

    def test_unconfigure_platform_inspect_disable_all(self):
        self.device = Mock()
        unconfigure_platform_inspect_disable_all(self.device)
        self.device.configure.assert_called_once_with(
            "no platform inspect disable-all"
        )
