from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import unconfigure_alarm_profile
from unittest.mock import Mock


class TestUnconfigureAlarmProfile(TestCase):

    def test_unconfigure_alarm_profile(self):
        self.device = Mock()
        result = unconfigure_alarm_profile(self.device, 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no alarm-profile test'],)
        )
