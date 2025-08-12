from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_facility_alarm_power_supply_relay
from unittest.mock import Mock


class TestConfigureFacilityAlarmPowerSupplyRelay(TestCase):

    def test_configure_facility_alarm_power_supply_relay(self):
        self.device = Mock()
        result = configure_facility_alarm_power_supply_relay(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('alarm facility power-supply relay major',)
        )
