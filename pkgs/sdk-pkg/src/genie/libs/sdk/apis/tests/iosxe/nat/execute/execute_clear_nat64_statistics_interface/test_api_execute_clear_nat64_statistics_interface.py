from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.nat.execute import (
    execute_clear_nat64_statistics_interface,
)


class TestExecuteClearNat64StatisticsInterface(TestCase):

    def test_execute_clear_nat64_statistics_interface(self):
        device = Mock()
        result = execute_clear_nat64_statistics_interface(
            device,
            'TenGigabitEthernet1/2/0/35',
        )

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            'clear nat64 statistics interface TenGigabitEthernet1/2/0/35'
        )
