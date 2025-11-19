from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_crypto_pki_certificate_map
from unittest.mock import Mock


class TestUnconfigureCryptoPkiCertificateMap(TestCase):

    def test_unconfigure_crypto_pki_certificate_map(self):
        self.device = Mock()
        result = unconfigure_crypto_pki_certificate_map(self.device, 'test_map', 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto pki certificate map test_map 10'],)
        )
