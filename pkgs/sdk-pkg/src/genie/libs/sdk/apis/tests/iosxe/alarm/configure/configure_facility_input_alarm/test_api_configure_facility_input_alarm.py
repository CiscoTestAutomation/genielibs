from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_facility_input_alarm
from unittest.mock import Mock


class TestConfigureFacilityInputAlarm(TestCase):

    def test_configure_facility_input_alarm(self):
        self.device = Mock()
        result = configure_facility_input_alarm(self.device, '1', False, False, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['alarm facility input-alarm 1 relay major'],)
        )
