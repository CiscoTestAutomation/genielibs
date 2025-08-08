from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.alarm.configure import unconfigure_facility_alarm_sdcard_relay
from unittest.mock import Mock


class TestUnconfigureFacilityAlarmSdcardRelay(TestCase):

    def test_unconfigure_facility_alarm_sdcard_relay(self):
        self.device = Mock()
        result = unconfigure_facility_alarm_sdcard_relay(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no alarm facility sd-card relay major',)
        )
