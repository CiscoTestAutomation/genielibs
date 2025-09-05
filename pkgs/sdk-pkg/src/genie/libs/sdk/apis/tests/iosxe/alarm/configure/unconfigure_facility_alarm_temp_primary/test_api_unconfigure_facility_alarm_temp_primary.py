from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import unconfigure_facility_alarm_temp_primary
from unittest.mock import Mock


class TestUnconfigureFacilityAlarmTempPrimary(TestCase):

    def test_unconfigure_facility_alarm_temp_primary(self):
        self.device = Mock()
        result = unconfigure_facility_alarm_temp_primary(self.device, None, None, False, True, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no alarm facility temperature primary syslog'],)
        )
