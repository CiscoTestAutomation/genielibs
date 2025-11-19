from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_crypto_pki_download_crl
from unittest.mock import Mock


class TestUnconfigureCryptoPkiDownloadCrl(TestCase):

    def test_unconfigure_crypto_pki_download_crl(self):
        self.device = Mock()
        result = unconfigure_crypto_pki_download_crl(self.device, False, False, False, None, False, None, False, 'Mon', None, 'root', False, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto pki crl download trustpoint root'],)
        )
