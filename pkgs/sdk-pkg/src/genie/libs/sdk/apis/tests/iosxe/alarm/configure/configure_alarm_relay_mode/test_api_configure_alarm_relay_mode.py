from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_alarm_relay_mode
from unittest.mock import Mock


class TestConfigureAlarmRelayMode(TestCase):

    def test_configure_alarm_relay_mode(self):
        self.device = Mock()
        result = configure_alarm_relay_mode(self.device, 'negative')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['alarm relay-mode negative'],)
        )
