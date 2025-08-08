from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.alarm.configure import configure_facility_alarm_sdcard_syslog
from unittest.mock import Mock


class TestConfigureFacilityAlarmSdcardSyslog(TestCase):

    def test_configure_facility_alarm_sdcard_syslog(self):
        self.device = Mock()
        result = configure_facility_alarm_sdcard_syslog(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('alarm facility sd-card syslog',)
        )
