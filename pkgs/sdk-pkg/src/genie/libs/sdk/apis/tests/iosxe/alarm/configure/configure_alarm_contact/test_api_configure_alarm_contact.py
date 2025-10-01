from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import configure_alarm_contact
from unittest.mock import Mock


class TestConfigureAlarmContact(TestCase):

    def test_configure_alarm_contact(self):
        self.device = Mock()
        result = configure_alarm_contact(self.device, '1', True, False, False, 'Configured by pyATS', 'major', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['alarm contact 1 description Configured by pyATS'],)
        )
