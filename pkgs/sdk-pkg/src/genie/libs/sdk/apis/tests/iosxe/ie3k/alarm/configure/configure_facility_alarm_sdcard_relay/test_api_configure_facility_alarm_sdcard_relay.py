from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.alarm.configure import configure_facility_alarm_sdcard_relay
from unittest.mock import Mock


class TestConfigureFacilityAlarmSdcardRelay(TestCase):

    def test_configure_facility_alarm_sdcard_relay(self):
        self.device = Mock()
        result = configure_facility_alarm_sdcard_relay(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('alarm facility sd-card relay major',)
        )
