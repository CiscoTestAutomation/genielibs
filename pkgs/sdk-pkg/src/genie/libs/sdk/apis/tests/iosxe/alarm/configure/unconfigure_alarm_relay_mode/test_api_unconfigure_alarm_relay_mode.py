from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import unconfigure_alarm_relay_mode
from unittest.mock import Mock


class TestUnconfigureAlarmRelayMode(TestCase):

    def test_unconfigure_alarm_relay_mode(self):
        self.device = Mock()
        result = unconfigure_alarm_relay_mode(self.device, 'negative')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no alarm relay-mode negative'],)
        )
