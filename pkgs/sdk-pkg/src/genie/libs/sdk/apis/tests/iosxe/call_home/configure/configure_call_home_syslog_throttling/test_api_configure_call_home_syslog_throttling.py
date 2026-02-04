from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.call_home.configure import configure_call_home_syslog_throttling


class TestConfigureCallHomeSyslogThrottling(TestCase):

    def test_configure_call_home_syslog_throttling(self):
        device = Mock()
        result = configure_call_home_syslog_throttling(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['call-home', 'syslog-throttling'],)
        )
