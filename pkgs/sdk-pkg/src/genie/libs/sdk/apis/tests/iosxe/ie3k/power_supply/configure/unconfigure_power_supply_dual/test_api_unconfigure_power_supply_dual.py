from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.power_supply.configure import unconfigure_power_supply_dual
from unittest.mock import Mock


class TestUnconfigurePowerSupplyDual(TestCase):

    def test_unconfigure_power_supply_dual(self):
        self.device = Mock()
        result = unconfigure_power_supply_dual(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no power-supply dual',)
        )
