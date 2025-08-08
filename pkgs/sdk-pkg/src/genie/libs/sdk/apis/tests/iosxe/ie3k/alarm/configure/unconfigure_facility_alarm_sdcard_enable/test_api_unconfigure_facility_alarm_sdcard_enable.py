from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.alarm.configure import unconfigure_facility_alarm_sdcard_enable
from unittest.mock import Mock


class TestUnconfigureFacilityAlarmSdcardEnable(TestCase):

    def test_unconfigure_facility_alarm_sdcard_enable(self):
        self.device = Mock()
        result = unconfigure_facility_alarm_sdcard_enable(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no alarm facility sd-card enable',)
        )
