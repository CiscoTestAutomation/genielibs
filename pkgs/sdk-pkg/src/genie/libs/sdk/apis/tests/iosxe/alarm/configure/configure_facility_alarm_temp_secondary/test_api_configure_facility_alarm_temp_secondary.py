from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_facility_alarm_temp_secondary
from unittest.mock import Mock


class TestConfigureFacilityAlarmTempSecondary(TestCase):

    def test_configure_facility_alarm_temp_secondary(self):
        self.device = Mock()
        result = configure_facility_alarm_temp_secondary(self.device, None, None, False, True, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['alarm facility temperature secondary syslog'],)
        )
