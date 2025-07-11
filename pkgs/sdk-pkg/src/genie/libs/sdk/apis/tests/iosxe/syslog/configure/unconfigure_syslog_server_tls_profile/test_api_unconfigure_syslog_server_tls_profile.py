from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import unconfigure_syslog_server_tls_profile
from unittest.mock import Mock


class TestUnconfigureSyslogServerTlsProfile(TestCase):

    def test_unconfigure_syslog_server_tls_profile(self):
        self.device = Mock()
        result = unconfigure_syslog_server_tls_profile(self.device, '10.64.69.167', 'syslog_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no logging host 10.64.69.167 transport tls profile syslog_1',)
        )
