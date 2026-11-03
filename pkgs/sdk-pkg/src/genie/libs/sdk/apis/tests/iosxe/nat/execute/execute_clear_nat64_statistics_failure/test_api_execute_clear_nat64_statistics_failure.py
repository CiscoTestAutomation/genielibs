from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nat.execute import (
    execute_clear_nat64_statistics_failure,
)


class TestExecuteClearNat64StatisticsFailure(TestCase):

    def test_execute_clear_nat64_statistics_failure(self):
        device = Mock()
        result = execute_clear_nat64_statistics_failure(device)

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear nat64 statistics failure'
        )
