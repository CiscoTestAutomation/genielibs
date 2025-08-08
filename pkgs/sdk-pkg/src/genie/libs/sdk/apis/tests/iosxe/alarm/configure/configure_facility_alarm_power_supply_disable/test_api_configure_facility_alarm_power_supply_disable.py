from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_facility_alarm_power_supply_disable
from unittest.mock import Mock


class TestConfigureFacilityAlarmPowerSupplyDisable(TestCase):

    def test_configure_facility_alarm_power_supply_disable(self):
        self.device = Mock()
        result = configure_facility_alarm_power_supply_disable(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('alarm facility power-supply disable',)
        )
