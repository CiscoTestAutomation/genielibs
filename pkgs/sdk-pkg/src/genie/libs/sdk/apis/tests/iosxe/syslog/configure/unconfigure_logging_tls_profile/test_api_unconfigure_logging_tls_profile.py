from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import unconfigure_logging_tls_profile
from unittest.mock import Mock


class TestUnconfigureLoggingTlsProfile(TestCase):

    def test_unconfigure_logging_tls_profile(self):
        self.device = Mock()
        result = unconfigure_logging_tls_profile(self.device, 'syslog_2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no logging tls-profile syslog_2'],)
        )
