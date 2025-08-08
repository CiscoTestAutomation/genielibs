from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.power_supply.configure import configure_power_supply_dual
from unittest.mock import Mock


class TestConfigurePowerSupplyDual(TestCase):

    def test_configure_power_supply_dual(self):
        self.device = Mock()
        result = configure_power_supply_dual(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('power-supply dual',)
        )
