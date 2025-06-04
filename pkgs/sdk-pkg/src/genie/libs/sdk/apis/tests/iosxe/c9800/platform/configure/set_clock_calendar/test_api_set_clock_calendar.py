from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.configure import set_clock_calendar


class TestSetClockCalendar(TestCase):

    def test_set_clock_calendar(self):
        self.device = Mock()
        result = set_clock_calendar(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('clock calendar-valid',)
        )
