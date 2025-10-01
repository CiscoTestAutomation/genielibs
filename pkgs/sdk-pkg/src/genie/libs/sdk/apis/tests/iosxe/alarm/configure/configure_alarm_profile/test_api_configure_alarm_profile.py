from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_alarm_profile
from unittest.mock import Mock


class TestConfigureAlarmProfile(TestCase):

    def test_configure_alarm_profile(self):
        self.device = Mock()
        result = configure_alarm_profile(self.device, 'test', 'no', [1, 2, 3, 4, 5, 6, 'fcs-error', 'link-fault'], 'notifies')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['alarm-profile test', 'no notifies 1', 'no notifies 2', 'no notifies 3', 'no notifies 4', 'no notifies 5', 'no notifies 6', 'no notifies fcs-error', 'no notifies link-fault'],)
        )
