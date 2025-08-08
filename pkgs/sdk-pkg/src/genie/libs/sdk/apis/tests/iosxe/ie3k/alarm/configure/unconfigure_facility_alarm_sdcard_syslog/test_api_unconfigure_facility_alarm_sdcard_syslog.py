from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.alarm.configure import unconfigure_facility_alarm_sdcard_syslog
from unittest.mock import Mock


class TestUnconfigureFacilityAlarmSdcardSyslog(TestCase):

    def test_unconfigure_facility_alarm_sdcard_syslog(self):
        self.device = Mock()
        result = unconfigure_facility_alarm_sdcard_syslog(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no alarm facility sd-card syslog',)
        )
