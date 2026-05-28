import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_set_clock_calendar


class TestConfigureSetClockCalendar(unittest.TestCase):

    def test_configure_set_clock_calendar(self):
        device = Mock()

        result = configure_set_clock_calendar(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('clock calendar-valid',)
        )