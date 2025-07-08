from unittest import TestCase
from genie.libs.sdk.apis.iosxe.syslog.configure import change_cipher_from_tls_profile
from unittest.mock import Mock


class TestChangeCipherFromTlsProfile(TestCase):

    def test_change_cipher_from_tls_profile(self):
        self.device = Mock()
        result = change_cipher_from_tls_profile(self.device, 'syslog_1', 'tls13-aes128-gcm-sha256')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['logging tls-profile syslog_1', 'no ciphersuite', 'ciphersuite tls13-aes128-gcm-sha256'],)
        )
