from unittest import TestCase
from genie.libs.sdk.apis.iosxe.logging.configure import configure_logging_alarm
from unittest.mock import Mock


class TestConfigureLoggingAlarm(TestCase):

    def test_configure_logging_alarm(self):
        self.device = Mock()
        result = configure_logging_alarm(self.device, 1)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('logging alarm 1',)
        )
