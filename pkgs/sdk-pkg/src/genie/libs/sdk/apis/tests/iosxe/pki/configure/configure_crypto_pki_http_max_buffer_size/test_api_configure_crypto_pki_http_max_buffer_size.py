from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.configure import configure_crypto_pki_http_max_buffer_size
from unittest.mock import Mock


class TestConfigureCryptoPkiHttpMaxBufferSize(TestCase):

    def test_configure_crypto_pki_http_max_buffer_size(self):
        self.device = Mock()
        result = configure_crypto_pki_http_max_buffer_size(self.device, 10)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto pki http max-buffer-size 10'],)
        )
