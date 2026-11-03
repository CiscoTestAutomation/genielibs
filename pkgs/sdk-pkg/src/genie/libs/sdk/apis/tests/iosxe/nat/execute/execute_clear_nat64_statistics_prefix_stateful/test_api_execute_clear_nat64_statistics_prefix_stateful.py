from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nat.execute import (
    execute_clear_nat64_statistics_prefix_stateful,
)


class TestExecuteClearNat64StatisticsPrefixStateful(TestCase):

    def test_execute_clear_nat64_statistics_prefix_stateful(self):
        device = Mock()
        result = execute_clear_nat64_statistics_prefix_stateful(
            device,
            '2001:1::',
            64,
        )

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear nat64 statistics prefix stateful 2001:1::/64'
        )
