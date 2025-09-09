from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import unconfigure_crypto_pki_http_max_buffer_size
from unittest.mock import Mock


class TestUnconfigureCryptoPkiHttpMaxBufferSize(TestCase):

    def test_unconfigure_crypto_pki_http_max_buffer_size(self):
        self.device = Mock()
        result = unconfigure_crypto_pki_http_max_buffer_size(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no crypto pki http max-buffer-size'],)
        )
