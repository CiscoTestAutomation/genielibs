from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_clock_timezone


class TestConfigureClockTimezone(TestCase):

    def test_configure_clock_timezone(self):
        device = Mock()
        result = configure_clock_timezone(
            device,
            'IST',
            5,
            30
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('clock timezone IST 5 30',)
        )