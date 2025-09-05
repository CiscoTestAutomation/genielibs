from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_crl_request
from unittest.mock import Mock


class TestConfigureCryptoPkiCrlRequest(TestCase):

    def test_configure_crypto_pki_crl_request(self):
        self.device = Mock()
        result = configure_crypto_pki_crl_request(self.device, 'root')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('crypto pki crl request root',)
        )
