from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import unconfigure_facility_alarm_power_supply_relay
from unittest.mock import Mock


class TestUnconfigureFacilityAlarmPowerSupplyRelay(TestCase):

    def test_unconfigure_facility_alarm_power_supply_relay(self):
        self.device = Mock()
        result = unconfigure_facility_alarm_power_supply_relay(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no alarm facility power-supply relay major',)
        )
