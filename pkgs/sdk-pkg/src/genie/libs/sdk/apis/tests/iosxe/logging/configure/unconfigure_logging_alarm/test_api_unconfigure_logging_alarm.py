from unittest import TestCase
from genie.libs.sdk.apis.iosxe.logging.configure import unconfigure_logging_alarm
from unittest.mock import Mock


class TestUnconfigureLoggingAlarm(TestCase):

    def test_unconfigure_logging_alarm(self):
        self.device = Mock()
        result = unconfigure_logging_alarm(self.device, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no logging alarm 1',)
        )
