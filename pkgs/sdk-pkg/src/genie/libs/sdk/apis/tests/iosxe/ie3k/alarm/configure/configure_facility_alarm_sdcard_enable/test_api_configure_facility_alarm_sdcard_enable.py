from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.alarm.configure import configure_facility_alarm_sdcard_enable
from unittest.mock import Mock


class TestConfigureFacilityAlarmSdcardEnable(TestCase):

    def test_configure_facility_alarm_sdcard_enable(self):
        self.device = Mock()
        result = configure_facility_alarm_sdcard_enable(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('alarm facility sd-card enable',)
        )
