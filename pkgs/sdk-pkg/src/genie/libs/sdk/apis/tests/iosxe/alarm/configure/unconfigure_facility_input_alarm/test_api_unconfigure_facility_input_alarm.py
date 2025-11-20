from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import unconfigure_facility_input_alarm
from unittest.mock import Mock


class TestUnconfigureFacilityInputAlarm(TestCase):

    def test_unconfigure_facility_input_alarm(self):
        self.device = Mock()
        result = unconfigure_facility_input_alarm(self.device, '1', False, False, True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no alarm facility input-alarm 1 relay major'],)
        )
