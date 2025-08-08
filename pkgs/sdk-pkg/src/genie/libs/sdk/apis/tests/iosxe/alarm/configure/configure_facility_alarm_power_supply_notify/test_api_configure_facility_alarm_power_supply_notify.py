from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_facility_alarm_power_supply_notify
from unittest.mock import Mock


class TestConfigureFacilityAlarmPowerSupplyNotify(TestCase):

    def test_configure_facility_alarm_power_supply_notify(self):
        self.device = Mock()
        result = configure_facility_alarm_power_supply_notify(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('alarm facility power-supply notifies',)
        )
