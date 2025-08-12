from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import unconfigure_facility_alarm_power_supply_syslog
from unittest.mock import Mock


class TestUnconfigureFacilityAlarmPowerSupplySyslog(TestCase):

    def test_unconfigure_facility_alarm_power_supply_syslog(self):
        self.device = Mock()
        result = unconfigure_facility_alarm_power_supply_syslog(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no alarm facility power-supply syslog',)
        )
