from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import configure_syslog_server
from unittest.mock import Mock


class TestConfigureSyslogServer(TestCase):

    def test_configure_syslog_server(self):
        self.device = Mock()
        result = configure_syslog_server(self.device, '10.64.49.167', 'tls', 'None')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('logging host 10.64.49.167 vrf None transport tls',)
        )
