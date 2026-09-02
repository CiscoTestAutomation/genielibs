from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import (
    configure_platform_inspect_disable_all,
)


class TestConfigurePlatformInspectDisableAll(TestCase):

    def test_configure_platform_inspect_disable_all(self):
        self.device = Mock()
        configure_platform_inspect_disable_all(self.device)
        self.device.configure.assert_called_once_with(
            "platform inspect disable-all"
        )
