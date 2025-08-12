from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.alarm.configure import unconfigure_facility_alarm_sdcard_notifies
from unittest.mock import Mock


class TestUnconfigureFacilityAlarmSdcardNotifies(TestCase):

    def test_unconfigure_facility_alarm_sdcard_notifies(self):
        self.device = Mock()
        result = unconfigure_facility_alarm_sdcard_notifies(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no alarm facility sd-card notifies',)
        )
