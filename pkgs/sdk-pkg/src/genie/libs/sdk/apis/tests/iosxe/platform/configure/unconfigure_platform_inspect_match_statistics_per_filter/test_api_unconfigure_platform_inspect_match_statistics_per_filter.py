from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import (
    unconfigure_platform_inspect_match_statistics_per_filter,
)


class TestUnconfigurePlatformInspectMatchStatisticsPerFilter(TestCase):

    def test_unconfigure_platform_inspect_match_statistics_per_filter(self):
        self.device = Mock()
        unconfigure_platform_inspect_match_statistics_per_filter(self.device)
        self.device.configure.assert_called_once_with(
            "no platform inspect match-statistics per-filter"
        )
