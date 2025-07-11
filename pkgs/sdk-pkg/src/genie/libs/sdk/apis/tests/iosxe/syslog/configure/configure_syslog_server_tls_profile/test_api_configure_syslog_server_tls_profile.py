from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import configure_syslog_server_tls_profile
from unittest.mock import Mock


class TestConfigureSyslogServerTlsProfile(TestCase):

    def test_configure_syslog_server_tls_profile(self):
        self.device = Mock()
        result = configure_syslog_server_tls_profile(self.device, '10.64.69.167', 'syslog_2', 'None')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('logging host 10.64.69.167 vrf None transport tls profile syslog_2',)
        )
