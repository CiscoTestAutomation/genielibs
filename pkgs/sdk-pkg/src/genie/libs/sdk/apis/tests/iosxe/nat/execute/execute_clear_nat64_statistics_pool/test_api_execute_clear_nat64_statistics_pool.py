from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nat.execute import (
    execute_clear_nat64_statistics_pool,
)


class TestExecuteClearNat64StatisticsPool(TestCase):

    def test_execute_clear_nat64_statistics_pool(self):
        device = Mock()
        result = execute_clear_nat64_statistics_pool(device, 'pool_1')

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear nat64 statistics pool pool_1'
        )
