from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_remote_span_monitor_session
from unittest.mock import Mock


class TestConfigureRemoteSpanMonitorSession(TestCase):

    def test_configure_remote_span_monitor_session(self):
        self.device = Mock()
        result = configure_remote_span_monitor_session(self.device, '30', 'destination', 'TwentyFiveGigE2/6/0/39', None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['monitor session 30 destination interface TwentyFiveGigE2/6/0/39'],)
        )
