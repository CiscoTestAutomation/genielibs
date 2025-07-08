from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import configure_logging_tls_profile
from unittest.mock import Mock


class TestConfigureLoggingTlsProfile(TestCase):

    def test_configure_logging_tls_profile(self):
        self.device = Mock()
        result = configure_logging_tls_profile(self.device, 'syslog_2', 'TLSv1.3', 'tls13-aes128-gcm-sha256', 'tp1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['logging tls-profile syslog_2', 'client-id-trustpoint tp1', 'ciphersuite tls13-aes128-gcm-sha256', 'tls-version TLSv1.3'],)
        )
