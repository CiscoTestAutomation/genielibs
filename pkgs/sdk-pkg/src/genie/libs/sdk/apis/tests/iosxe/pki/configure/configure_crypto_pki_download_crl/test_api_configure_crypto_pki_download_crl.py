from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_download_crl
from unittest.mock import Mock


class TestConfigureCryptoPkiDownloadCrl(TestCase):

    def test_configure_crypto_pki_download_crl(self):
        self.device = Mock()
        result = configure_crypto_pki_download_crl(self.device, False, False, False, None, False, None, False, None, None, 'root', False, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki crl download trustpoint root'],)
        )
