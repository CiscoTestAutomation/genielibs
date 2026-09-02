from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import (
    configure_platform_inspect_match_statistics_per_filter,
)


class TestConfigurePlatformInspectMatchStatisticsPerFilter(TestCase):

    def test_configure_platform_inspect_match_statistics_per_filter(self):
        self.device = Mock()
        configure_platform_inspect_match_statistics_per_filter(self.device)
        self.device.configure.assert_called_once_with(
            "platform inspect match-statistics per-filter"
        )
