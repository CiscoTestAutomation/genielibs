from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_certificate_map
from unittest.mock import Mock


class TestConfigureCryptoPkiCertificateMap(TestCase):

    def test_configure_crypto_pki_certificate_map(self):
        self.device = Mock()
        result = configure_crypto_pki_certificate_map(self.device, 'test_map', 10, True, 'co', 'co', 'test_issuer', True, 'test_subject', False, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki certificate map test_map 10', 'issuer-name co test_issuer', 'subject-name co test_subject'],)
        )
