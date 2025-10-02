from unittest import TestCase
from genie.libs.sdk.apis.iosxe.alarm.configure import unconfigure_alarm_contact
from unittest.mock import Mock


class TestUnconfigureAlarmContact(TestCase):

    def test_unconfigure_alarm_contact(self):
        self.device = Mock()
        result = unconfigure_alarm_contact(self.device, '1', True, False, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no alarm contact 1 description'],)
        )
